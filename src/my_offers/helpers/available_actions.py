from typing import Optional

from simple_settings import settings

from my_offers import entities
from my_offers.entities import AgentHierarchyData
from my_offers.enums import OfferPayedByType
from my_offers.repositories.agencies_settings.entities import AgencySettings
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Status


CAN_ARCHIVE_STATUSES = (Status.deactivated, Status.published, Status.draft)
CAN_CHANGE_PUBLISHER = (Status.published, Status.deactivated, Status.draft, Status.sold)
CAN_DELETE_STATUSES = (
    Status.published,
    Status.draft,
    Status.blocked,
    Status.deactivated,
    Status.refused
)
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
        agent_hierarchy_data: AgentHierarchyData,
        force_raise: bool = False,
        can_view_similar_offers: bool = False,
        payed_by: Optional[OfferPayedByType] = None
) -> entities.AvailableActions:
    """
        Получить возможные действия с объявлением.

        Активные: Удалить, Перенести в архив, Редактировать, Поднять, Сменить владельца (только мастер)
        Неактивные: Удалить, Перенести в архив, Редактировать(черновик),
                    Восстановить (!= черновик), Сменить владельца (только мастер)
        Архив: Восстановить, Удалить

        Если объявление находится в статусе `Снято с публикации`, то появляется кнопка "Восстановить".
        Если объявление находится в статусе `Черновик`, то появляется кнопка "Редактировать".
        Объявления агентов, которые оплачены за их счет и отображаются мастеру, недоступны для редактирования.

        Дополнительно доступ для иерархии:
        https://docs.google.com/spreadsheets/d/1QPcPU4vxK1_PBj1HXcsYsQk9iL07kiF8pC_kcsMLU3k/edit#gid=174751677
    """
    if not status:
        status = Status.deleted

    if agent_hierarchy_data.is_master_agent and payed_by == OfferPayedByType.by_agent:
        return entities.AvailableActions(
            can_edit=False,
            can_raise=False,
            can_raise_without_addform=False,
            can_delete=False,
            can_restore=False,
            can_update_edit_date=False,
            can_move_to_archive=False,
            can_change_publisher=False,
            can_view_similar_offers=False
        )

    if not is_manual:
        can_edit = agency_settings.can_sub_agents_edit_offers_from_xml if agency_settings else False
        return entities.AvailableActions(
            can_edit=not is_archived and can_edit,
            can_raise=not is_archived and status.is_published and can_edit,
            can_raise_without_addform=_can_raise_without_addform(
                agent_hierarchy_data=agent_hierarchy_data,
                force_raise=force_raise,
                is_archived=is_archived,
                is_published=status.is_published,
                is_in_hidden_base=is_in_hidden_base
            ),
            can_delete=False,
            can_restore=False,
            can_update_edit_date=False,
            can_move_to_archive=False,
            can_change_publisher=False,
            can_view_similar_offers=can_view_similar_offers
        )

    can_edit = not is_archived and not status.is_removed_by_moderator
    can_change_publisher = not is_archived and agent_hierarchy_data.is_master_agent and status in CAN_CHANGE_PUBLISHER

    return entities.AvailableActions(
        can_edit=status.is_draft or status.is_published and can_edit,
        can_raise=_can_raise(
            force_raise=force_raise,
            is_archived=is_archived,
            is_published=status.is_published,
            is_in_hidden_base=is_in_hidden_base
        ),
        can_raise_without_addform=_can_raise_without_addform(
            agent_hierarchy_data=agent_hierarchy_data,
            force_raise=force_raise,
            is_archived=is_archived,
            is_published=status.is_published,
            is_in_hidden_base=is_in_hidden_base
        ),
        can_delete=_can_delete(
            is_archived=is_archived,
            status=status
        ),
        can_restore=_can_restore(
            is_archived=is_archived,
            is_removed_by_moderator=status.is_removed_by_moderator,
            is_discontinued=status in STATUSES_FOR_DISCONTINUED
        ),
        can_update_edit_date=not is_archived and status.is_published and can_update_edit_date,
        can_move_to_archive=not is_archived and status in CAN_ARCHIVE_STATUSES,
        can_change_publisher=can_change_publisher,
        can_view_similar_offers=can_view_similar_offers
    )


def _can_delete(*, is_archived: bool, status: Status) -> bool:
    if is_archived and status.removed_by_moderator:
        return True

    return status in CAN_DELETE_STATUSES


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


def _can_raise_without_addform(
        *,
        agent_hierarchy_data: AgentHierarchyData,
        is_archived: bool,
        is_published: bool,
        is_in_hidden_base: Optional[bool],
        force_raise: bool,
) -> bool:
    can_raise_settings = settings.CAN_RAISE_WITHOUT_ADDFORM or []

    if agent_hierarchy_data.is_master_agent and 'master_agent' in can_raise_settings:
        return _can_raise(
            is_archived=is_archived,
            is_published=is_published,
            is_in_hidden_base=is_in_hidden_base,
            force_raise=force_raise,
        )

    if agent_hierarchy_data.is_sub_agent and 'sub_agent' in can_raise_settings:
        return _can_raise(
            is_archived=is_archived,
            is_published=is_published,
            is_in_hidden_base=is_in_hidden_base,
            force_raise=force_raise,
        )

    if agent_hierarchy_data.is_agent and 'agent' in can_raise_settings:
        return _can_raise(
            is_archived=is_archived,
            is_published=is_published,
            is_in_hidden_base=is_in_hidden_base,
            force_raise=force_raise,
        )

    return False
