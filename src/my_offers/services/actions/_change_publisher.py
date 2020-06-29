from my_offers import entities
from my_offers.repositories.monolith_cian_announcementapi.entities.announcement_progress_dto import (
    State as OffersOperationStatus,
)


async def change_offers_publisher(
    request: entities.OffersChangePublisherRequest,
    realty_user_id: int
):
    """ Сменить владельца для объялвений. Выполнить действие может только мастер аккаунт. """

    if not request.offers_ids:
        return entities.OffersChangePublisherResponse(offers=[])

    # TODO: Прокси и шарпу CD-84467
    return entities.OffersChangePublisherResponse(
        offers=[
            entities.OffersChangePublisherStatus(
                offer_id=3,
                status=OffersOperationStatus.completed,
            ),
            entities.OffersChangePublisherStatus(
                offer_id=4,
                status=OffersOperationStatus.error,
                message='Ошибка при смене владельца. Недостаточно средств.'
            )
        ]
    )
