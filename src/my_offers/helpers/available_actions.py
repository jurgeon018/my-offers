from typing import Optional

from my_offers import entities
from my_offers.repositories.agencies_settings.entities import AgencySettings
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Status


CAN_ARCHIVE_STATUSES = (Status.deactivated, Status.published, Status.draft)
CAN_DELETE_STATUSES = (Status.published, Status.draft, Status.blocked, Status.deactivated, Status.refused)


def get_available_actions(
        *,
        is_archived: bool,
        is_manual: bool,
        status: Optional[Status],
        can_update_edit_date: bool,
        agency_settings: Optional[AgencySettings],
        is_in_hidden_base: Optional[bool],
) -> entities.AvailableActions:
    # Возможные действия
    # Активные: Удалить, Перенести в архив, Редактировать, Поднять
    # Неактивные: Удалить, Перенести в архив, Редактировать
    # Архив: Восстановить, Удалить
    #
    # Дополнительно доступ для иерархии:
    # https://docs.google.com/spreadsheets/d/1QPcPU4vxK1_PBj1HXcsYsQk9iL07kiF8pC_kcsMLU3k/edit#gid=174751677

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
        )

    return entities.AvailableActions(
        can_edit=not is_archived and not status.is_removed_by_moderator,
        can_raise=not is_archived and status.is_published,
        can_delete=status in CAN_DELETE_STATUSES,
        can_restore=_can_restore(
            is_archived=is_archived,
            is_removed_by_moderator=status.is_removed_by_moderator,
            is_in_hidden_base=is_in_hidden_base,
        ),
        can_update_edit_date=not is_archived and status.is_published and can_update_edit_date,
        can_move_to_archive=not is_archived and status in CAN_ARCHIVE_STATUSES,
    )


def _can_restore(*, is_archived: bool, is_removed_by_moderator: bool, is_in_hidden_base: Optional[bool]) -> bool:
    if is_in_hidden_base:
        return False

    if is_removed_by_moderator:
        return False

    if not is_archived:
        return False

    return True
