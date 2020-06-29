from my_offers import entities
from my_offers.enums.change_publisher import ChangePublisherStatus


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
                status=ChangePublisherStatus.completed,
            ),
            entities.OffersChangePublisherStatus(
                offer_id=4,
                status=ChangePublisherStatus.error,
                message='Ошибка при смене владельца. Недостаточно средств.'
            )
        ]
    )
