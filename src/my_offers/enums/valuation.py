from cian_enum import StrEnum


class PriceEstimate(StrEnum):
    more_market = 'more_market'
    """Выше рынка"""
    in_market = 'in_market'
    """"В рынке"""
    less_market = 'less_market'
    """"Ниже рынка"""
