from cian_enum import StrEnum


class OfferPayedByType(StrEnum):
    """За чей счёт оплачена подача объявления"""
    by_master = 'by_master'
    by_agent = 'by_agent'
    