import logging

from cian_http.exceptions import ApiClientException
from cian_web.exceptions import BrokenRulesException, Error

from my_offers import entities, enums
from my_offers.repositories.monolith_cian_announcementapi.entities import ObjectModel
from my_offers.repositories.monolith_cian_realty import api_announcement_set_deleted
from my_offers.repositories.monolith_cian_realty.entities import AnnouncementChangeStatus
from my_offers.repositories.monolith_cian_realty.entities.announcement_change_status import AnnouncementType
from my_offers.repositories.postgresql.object_model import get_object_model
from my_offers.services.announcement import category
from my_offers.services.get_master_user_id import get_master_user_id


logger = logging.getLogger(__name__)

class AnnouncementTypeError(Exception):
    pass


async def delete_offer(request: entities.OfferActionRequest, realty_user_id: int) -> None:
    offer_id = request.offer_id
    object_model = await get_object_model({
        'offer_id': offer_id,
        'master_user_id': await get_master_user_id(realty_user_id),
    })
    if not object_model:
        raise BrokenRulesException([
            Error(
                message='Объявление не найдено',
                code='not_found',
                key='offer_id'
            )
        ])

    await _check_rights(user_id=realty_user_id, object_model=object_model)

    offer_type, deal_type = category.get_types(object_model.category)
    try:
        await api_announcement_set_deleted(
            AnnouncementChangeStatus(
                realty_object_id=offer_id,
                announcement_type=_get_type_for_asp(offer_type=offer_type, deal_type=deal_type),
                cian_announcement_id=object_model.cian_id,
            )
        )
    except ApiClientException as e:
        logger.exception('Delete offer %s error', offer_id)
        raise BrokenRulesException([
            Error(
                message=e.message,
                code='operation_error',
                key='offer_id'
            )
        ])


async def _check_rights(*, user_id: int, object_model: ObjectModel) -> None:
    # todo: https://jira.cian.tech/browse/CD-74186
    if user_id != object_model.user_id:
        raise BrokenRulesException([
            Error(
                message='Не хватает прав для выполнения данной операции',
                code='not_enough_rights',
                key='offer_id'
            )
        ])


def _get_type_for_asp(*, offer_type: enums.OfferType, deal_type: enums.DealType) -> AnnouncementType:
    if offer_type.is_flat:
        return AnnouncementType.flat if deal_type.is_rent else AnnouncementType.flat2

    if offer_type.is_suburban:
        return AnnouncementType.suburbian

    if offer_type.is_commercial:
        return AnnouncementType.office

    raise AnnouncementTypeError('Сan not determine AnnouncementType')
