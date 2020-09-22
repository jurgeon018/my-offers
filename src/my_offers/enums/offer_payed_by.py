from cian_enum import StrEnum


class OfferPayedBy(StrEnum):
    by_master = 'by_master'
    """Архив"""
    by_agent = 'by_agent'
    """Удалено"""
