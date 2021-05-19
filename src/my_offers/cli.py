from functools import partial

import click
from cian_core.context import new_operation_id
from cian_core.rabbitmq.consumer_cli import register_consumer
from cian_core.web import Application
from tornado.ioloop import IOLoop

from my_offers import setup
from my_offers.helpers.schemas import get_entity_schema
from my_offers.queue import consumers, entities as mq_entities, queues, schemas
from my_offers.services import realty_resender
from my_offers.services.duplicates import sync_offer_duplicates
from my_offers.services.offers import delete_offers_data, reindex_offers_command, sync_offers
from my_offers.services.users import clean_users
from my_offers.web.urls import urlpatterns


@click.group()
def cli() -> None:
    setup()


@cli.command()
@click.option('--debug', is_flag=True)
@click.option('--host', type=str, default='127.0.0.1')
@click.option('--port', type=int, default=8000)
def serve(debug: bool, host: str, port: int) -> None:
    app = Application(urlpatterns, debug=debug)
    app.start(host=host, port=port)


# [announcements] обновляет объявление
register_consumer(
    command=cli.command('process_announcement_consumer'),
    queue=queues.process_announcements_queue,
    callback=consumers.process_announcement_callback,
    schema_cls=schemas.RabbitMQAnnouncementMessageSchema,
    dead_queue_enabled=True,
)

# [announcements-temp] очередь догонки объявлений через `resend` API
register_consumer(
    command=cli.command('process_announcement_from_temp_consumer'),
    queue=queues.process_announcements_from_temp,
    callback=consumers.process_announcement_callback,
    schema_cls=schemas.RabbitMQAnnouncementMessageSchema,
    dead_queue_enabled=True,
)

# [my-offers] очередь догонки объявлений через elasticapi на стороне my-offers
register_consumer(
    command=cli.command('process_announcement_from_elasticapi_consumer'),
    queue=queues.process_announcements_from_elasticapi,
    callback=consumers.process_announcement_callback,
    schema_cls=schemas.RabbitMQAnnouncementMessageSchema,
    dead_queue_enabled=True,
)

# [billing] сохраняет/обновляет контракты по объявлению
register_consumer(
    command=cli.command('save_announcement_contract_consumer'),
    queue=queues.save_announcement_contract_queue,
    callback=consumers.save_announcement_contract_callback,
    schema_cls=schemas.RabbitMQServiceContractCreatedMessageSchema,
    dead_queue_enabled=True,
)

# [billing] помечает закрытые контракты как удаленные
register_consumer(
    command=cli.command('mark_to_delete_announcement_contract_consumer'),
    queue=queues.close_announcement_contract_queue,
    callback=consumers.mark_to_delete_announcement_contract_callback,
    schema_cls=schemas.RabbitMQServiceContractCreatedMessageSchema,
    dead_queue_enabled=True,
)

# [import] сохраняет последнию ошибку импорта по объявлению
register_consumer(
    command=cli.command('save_offer_unload_error_consumer'),
    queue=queues.save_offer_unload_error_queue,
    callback=consumers.save_offer_unload_error_callback,
    schema_cls=schemas.RabbitMQSaveUnloadErrorMessageSchema,
    dead_queue_enabled=True,
)

# [moderation] сохраняет/обновляет нарушения по объявлениям
register_consumer(
    command=cli.command('save_moderation_offer_offence_consumer'),
    queue=queues.moderation_offence_queue,
    callback=consumers.save_offer_offence_callback,
    schema_cls=schemas.RabbitMQOffenceMessageSchema,
    dead_queue_enabled=True,
)

# [agents] сохраняет/обновляет данные об агентах
register_consumer(
    command=cli.command('save_agent_consumer'),
    queue=queues.update_agents_queue,
    callback=consumers.save_agent_callback,
    schema_cls=schemas.RabbitMQAgentUpdatedMessageSchema,
    dead_queue_enabled=True,
)

# [moderation] объявление отправлено на премодерацию
register_consumer(
    command=cli.command('save_offer_premoderation_consumer'),
    queue=queues.announcement_premoderation_sent_queue,
    callback=consumers.save_offer_premoderation_callback,
    schema_cls=schemas.RabbitMQAnnouncementPremoderationReportingMessageSchema,
    dead_queue_enabled=True,
)

# [moderation] объявление отмодерировано
register_consumer(
    command=cli.command('remove_offer_premoderation_consumer'),
    queue=queues.announcement_premoderation_remove_queue,
    callback=consumers.remove_offer_premoderation_callback,
    schema_cls=schemas.RabbitMQAnnouncementPremoderationReportingMessageSchema,
    dead_queue_enabled=True,
)

# [duplicates] обновление дублей
register_consumer(
    command=cli.command('update_offer_duplicates_consumer'),
    queue=queues.update_offer_duplicates_queue,
    callback=consumers.update_offer_duplicates_callback,
    schema_cls=schemas.RabbitMQNeedUpdateDuplicateMessageSchema,
    dead_queue_enabled=True,
)

# [duplicates] рассылка пушей по новым дубликатам
register_consumer(
    command=cli.command('new_offer_duplicate_notification_consumer'),
    queue=queues.new_offer_duplicate_notification_queue,
    callback=consumers.new_offer_duplicate_notification_callback,
    schema_cls=mq_entities.OfferNewDuplicateMessage,
    dead_queue_enabled=True,
    default_prefetch_count=1,
)

# [duplicates] пуши по изменению цены в дублях
register_consumer(
    command=cli.command('offer_duplicate_price_changed_notification_consumer'),
    queue=queues.offer_duplicate_price_changed_notification_queue,
    callback=consumers.offer_duplicate_price_changed_notification_callback,
    schema_cls=mq_entities.OfferDuplicatePriceChangedMessage,
    dead_queue_enabled=True,
    default_prefetch_count=1,
)

# [users] удаление данных пользователя
register_consumer(
    command=cli.command('delete_user_data_queue_consumer'),
    queue=queues.delete_user_data_queue,
    callback=consumers.delete_user_data_callback,
    schema_cls=get_entity_schema(mq_entities.DeleteUserDataMessage),
    dead_queue_enabled=True,
    default_prefetch_count=1,
)

# [offer_relevance_warnings] получение актуальности/неактуальности объявления
register_consumer(
    command=cli.command('save_offer_relevance_warning_consumer'),
    queue=queues.save_offer_relevance_warning_queue,
    callback=consumers.save_offer_relevance_warning_callback,
    schema_cls=get_entity_schema(mq_entities.OfferRelevanceWarningMessage),
    dead_queue_enabled=True,
)

register_consumer(
    command=cli.command('update_offer_master_user_consumer'),
    queue=queues.update_offer_master_user_queue,
    callback=consumers.update_offer_master_user_callback,
    schema_cls=get_entity_schema(mq_entities.UpdateOfferMasterUserMessage),
    dead_queue_enabled=True,
)

@cli.command()
def reindex_offers() -> None:
    """ Переиндексация объявлений """
    with new_operation_id():
        io_loop = IOLoop.current()
        io_loop.run_sync(reindex_offers_command)


@cli.command()
def clear_deleted_offer_cron() -> None:
    """Крон удаления офферов"""
    io_loop = IOLoop.current()
    io_loop.run_sync(delete_offers_data)


@cli.command()
@click.option('--bulk-size', type=int, default=50)
def resend_offers(bulk_size: int):
    """ Дослать объявления из Realty """

    IOLoop.current().run_sync(partial(
        realty_resender.resend_offers,
        bulk_size=bulk_size
    ))


@cli.command()
@click.option('--ids', type=str)
def fix_offers(ids: str):
    """ Догнать объявления до актуального статуса.

        my-offers fix-offers --ids 123,777
    """
    offers_ids = list(map(int, [i.strip() for i in ids.split(',')]))

    with new_operation_id():
        IOLoop.current().run_sync(partial(
            realty_resender.save_offers_from_elasticapi,
            offers_ids=offers_ids
        ))


@cli.command()
def sync_offer_duplicates_cron() -> None:
    """ Переодически сверяем данныо о дублях с МЛ """
    IOLoop.current().run_sync(sync_offer_duplicates)


@cli.command()
def clean_users_command() -> None:
    """
    Удаляет пользователей и объявления если не найдет их в МКС users"
    Предварительно надо сохранить id пользователей в таблицу users_reindex_queue
    """
    with new_operation_id():
        IOLoop.current().run_sync(clean_users)


@cli.command()
def sync_offers_command() -> None:
    """
    """
    with new_operation_id():
        IOLoop.current().run_sync(sync_offers)
