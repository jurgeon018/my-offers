from typing import Optional

from my_offers import entities
from my_offers.repositories.agencies_settings.entities import AgencySettings
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Status


CAN_ARCHIVE_STATUSES = (Status.deactivated, Status.published, Status.draft)
CAN_DELETE_STATUSES = (Status.published, Status.draft, Status.blocked, Status.deactivated, Status.refused)
CAN_CHANGE_PUBLISHER = (Status.published, Status.draft, Status.deactivated, Status.sold)
STATUSES_FOR_DISCONTINUED = (
    Status.deactivated,
    Status.deleted,
    Status.removed_by_moderator,
    Status.refused,
    Status.sold,
    Status.moderate,
    Status.blocked,
)


def get_available_actions(
        *,
        is_archived: bool,
        is_manual: bool,
        status: Optional[Status],
        can_update_edit_date: bool,
        agency_settings: Optional[AgencySettings],
        is_in_hidden_base: Optional[bool],
        is_master_agent: bool,
        force_raise: bool = False,
        can_view_similar_offers: bool = False
) -> entities.AvailableActions:
    """
        Получить возможные действия с объявлением.

        Активные: Удалить, Перенести в архив, Редактировать, Поднять, Сменить владельца (только мастер)
        Неактивные: Удалить, Перенести в архив, Редактировать(черновик),
                    Восстановить (!= черновик), Сменить владельца (только мастер)
        Архив: Восстановить, Удалить

        Если объявление находится в статусе `Снято с публикации`, то появляется кнопка "Восстановить".
        Если объявление находится в статусе `Черновик`, то появляется кнопка "Редактировать".

        Дополнительно доступ для иерархии:
        https://docs.google.com/spreadsheets/d/1QPcPU4vxK1_PBj1HXcsYsQk9iL07kiF8pC_kcsMLU3k/edit#gid=174751677
    """
    if not status:
        status = Status.deleted

    if not is_manual:
        can_edit = agency_settings.can_sub_agents_edit_offers_from_xml if agency_settings else False
        return entities.AvailableActions(
            can_edit=not is_archived and can_edit,
            can_raise=not is_archived and status.is_published and can_edit,
            can_delete=False,
            can_restore=False,
            can_update_edit_date=False,
            can_move_to_archive=False,
            can_change_publisher=False,
            can_view_similar_offers=can_view_similar_offers
        )

    can_edit = not is_archived and not status.is_removed_by_moderator
    return entities.AvailableActions(
        can_edit=status.is_draft or status.is_published and can_edit,
        can_raise=_can_raise(
            force_raise=force_raise,
            is_archived=is_archived,
            is_published=status.is_published,
            is_in_hidden_base=is_in_hidden_base
        ),
        can_delete=status in CAN_DELETE_STATUSES,
        can_restore=_can_restore(
            is_archived=is_archived,
            is_removed_by_moderator=status.is_removed_by_moderator,
            is_discontinued=status in STATUSES_FOR_DISCONTINUED
        ),
        can_update_edit_date=not is_archived and status.is_published and can_update_edit_date,
        can_move_to_archive=not is_archived and status in CAN_ARCHIVE_STATUSES,
        can_change_publisher=is_master_agent and status in CAN_CHANGE_PUBLISHER,
        can_view_similar_offers=can_view_similar_offers
    )


def _can_restore(*, is_archived: bool, is_removed_by_moderator: bool, is_discontinued: bool) -> bool:
    if is_removed_by_moderator:
        return False

    if is_archived or is_discontinued:
        return True

    return False


def _can_raise(*, is_archived: bool, is_published: bool, is_in_hidden_base: Optional[bool], force_raise: bool) -> bool:
    if force_raise:
        return True

    if is_archived:
        return False

    if not is_published:
        return False

    if is_in_hidden_base:
        return False

    return True
