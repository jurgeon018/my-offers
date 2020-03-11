from cian_enum import NoFormat, StrEnum


class OfferServices(StrEnum):
    __value_format__ = NoFormat
    top3 = 'top3'
    premium = 'premium'
    premium_highlight = 'premium+highlight'
    paid = 'paid'
    free = 'free'
    auction = 'auction'
