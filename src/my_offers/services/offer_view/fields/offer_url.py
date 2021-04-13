from simple_settings import settings

from my_offers import enums


def get_offer_url(
        *,
        cian_offer_id: int,
        offer_type: enums.OfferType,
        deal_type: enums.DealType
) -> str:
    """ Получить ссылку на объявление на сайте.
        Важно: при формировании сслыки нужно учитывать, что должен быть передан cian_id, а не realty_offer_id.
    """
    return f'{settings.CIAN_BASE_URL}/{deal_type.value}/{offer_type.value}/{cian_offer_id}/'
