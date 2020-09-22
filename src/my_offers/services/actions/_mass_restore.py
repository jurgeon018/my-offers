from typing import List, Tuple

from cian_web.exceptions import BrokenRulesException, Error
from simple_settings import settings

from my_offers import entities, helpers
from my_offers.enums import GetOffersSortType
from my_offers.repositories import monolith_cian_announcementapi, postgresql
from my_offers.repositories.monolith_cian_announcementapi.entities import (
    AnnouncementProgressDto,
    ObjectModel,
    RestoreRequest,
)
from my_offers.repositories.monolith_cian_announcementapi.entities.announcement_progress_dto import (
    State as OfferMassRestoreState,
)
from my_offers.services.actions._action import MassActions
from my_offers.services.offers import get_filters


class OffersMassRestoreAction(MassActions):

    async def _run_job(self) -> int:
        session = await monolith_cian_announcementapi.announcements_actions_v1_restore(
            RestoreRequest(
                announcement_ids=self.offers_ids,
                user_id=self.actor_id
            )
        )
        return session.job_id


async def mass_offers_restore(
        request: entities.OffersMassRestoreRequest,
        realty_user_id: int
) -> entities.OffersMassRestoreResponse:
    """ Массово восстановить все объявление для пользователя """
    offers_statuses = []

    if not request.offers_ids and request.action_type.is_select:
        raise BrokenRulesException(errors=[Error(
            key='offers_ids',
            code='offers_ids_is_empty',
            message=f'offers_ids is empty with type `{request.action_type.name}`'
        )])

    filters = await get_filters(
        user_id=realty_user_id,
        filters=request.filters
    )
    if request.action_type.is_select:
        filters['offer_id'] = request.offers_ids

    objects_models, total = await postgresql.get_object_models(
        filters=filters,
        limit=settings.MASS_OFFERS_LIMIT,
        offset=0,
        sort_type=GetOffersSortType.by_default
    )
    offers_ids, offers_errors, offers_counters = _filter_offers(objects_models=objects_models)
    offers_statuses.extend(offers_errors)

    if offers_ids:
        mass_restore_action = OffersMassRestoreAction(
            offers_ids=offers_ids,
            actor_id=realty_user_id
        )
        offers_final_statuses = await mass_restore_action.execute(
            delay=settings.MASS_OFFERS_RESTORE_DELAY
        )
        offers_statuses += [
            entities.OfferMassRestoreStatus(
                offer_id=offer.id,
                status=offer.state,
                message=offer.error_message
            ) for offer in offers_final_statuses
        ]

        restored_count, error_count = _get_result_counters(offers_final_statuses)
        offers_counters.restored_count = restored_count
        offers_counters.error_count = error_count

    return entities.OffersMassRestoreResponse(
        offers=offers_statuses,
        total=total,
        counters=offers_counters
    )


def _get_result_counters(results: List[AnnouncementProgressDto]) -> Tuple[int, int]:
    restored_count = 0
    error_count = 0

    for res in results:
        if res.state and res.state.is_error:
            error_count += 1
        elif res.state and res.state.is_completed:
            restored_count += 1

    return restored_count, error_count


def _filter_offers(
        objects_models: List[ObjectModel]
) -> Tuple[List[int], List[entities.OfferMassRestoreStatus], entities.OffersMassRestoreCounters]:
    offers_ids = []
    offers_errors = []
    offers_counters = entities.OffersMassRestoreCounters(draft_count=0, xml_count=0)

    for offer in objects_models:
        is_manual = helpers.is_manual(offer.source)
        is_draft = helpers.is_draft(offer.status)
        is_xml = not is_manual

        if is_xml:
            offers_counters.xml_count += 1
            offers_errors.append(entities.OfferMassRestoreStatus(
                offer_id=offer.id,
                status=OfferMassRestoreState.error,
                message='Нельзя автоматически восстановить XML'
            ))

        elif is_draft:
            offers_counters.draft_count += 1

        elif is_manual:
            offers_ids.append(offer.id)

    return offers_ids, offers_errors, offers_counters
