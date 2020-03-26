from attr import dataclass


@dataclass
class OfferPremoderation:
    offer_id: int
    """Id объявления"""
    removed: bool
    """Санкция снята"""
    row_version: int
    """Версия записи"""
