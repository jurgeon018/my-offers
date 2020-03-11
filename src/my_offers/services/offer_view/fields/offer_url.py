from simple_settings import settings

from my_offers import enums


def get_offer_url(
        *,
        offer_id: int,
        offer_type: enums.OfferType,
        deal_type: enums.DealType
) -> str:
    return f'{settings.CiAN_BASE_URL}/{deal_type.value}/{offer_type.value}/{offer_id}'
