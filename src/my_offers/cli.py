from datetime import timedelta

import click
from cian_core.rabbitmq.consumer_cli import register_consumer
from cian_core.web import Application
from tornado.ioloop import IOLoop

from my_offers import setup
from my_offers.queue import consumers, queues, schemas
from my_offers.services.offers.clear_offer_service import clear_deleted_offer
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


register_consumer(
    command=cli.command('process_announcement_consumer'),
    queue=queues.process_announcements_queue,
    callback=consumers.process_announcement_callback,
    schema_cls=schemas.RabbitMQAnnouncementMessageSchema,
    dead_queue_enabled=True,
    dead_queue_ttl=timedelta(seconds=60),
)


@cli.command()
def clear_deleted_offer_cron() -> None:
    """Крон удаления офферов"""
    io_loop = IOLoop.current()
    io_loop.run_sync(clear_deleted_offer)
