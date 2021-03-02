from cian_enum import StrEnum


class DeactivatedServicesContext(StrEnum):
    undefined = 'undefined'
    """Не определен"""
    highlight = 'highlight'
    """Выделение цветом"""
    auction = 'auction'
    """Аукцион"""
    highlight_and_auction = 'highlight_and_auction'
    """Выделение цветом и аукцион"""
