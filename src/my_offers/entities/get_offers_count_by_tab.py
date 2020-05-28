from dataclasses import dataclass

from my_offers.enums import OfferStatusTab


@dataclass
class GetOffersCountByTabRequest:
    status_tab: OfferStatusTab
    """Статус оффера"""
    user_id: int
    """RealtyId пользователя"""
    with_subs: bool
    """
    Считать объявки только для переданного user_id или для
    мастер-аккаунта переданного user_id и всех его саб-аккаунтов
    """


@dataclass
class GetOffersCountByTabResponse:
    count: int
