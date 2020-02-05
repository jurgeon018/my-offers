from cian_enum import NoFormat, StrEnum


class Services(StrEnum):
    __value_format__ = NoFormat
    free = 'free'
    highlight = 'highlight'
    paid = 'paid'
    premium = 'premium'
    top3 = 'top3'
    calltracking = 'calltracking'
    auction = 'auction'
