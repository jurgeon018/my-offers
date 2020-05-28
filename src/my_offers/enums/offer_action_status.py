from cian_enum import StrEnum


class OfferActionStatus(StrEnum):
    ok = 'ok'


class ActionType(StrEnum):
    all = 'all'
    """Восстановить все объявления"""
    select = 'select'
    """Восстановить выбранные объявления в offers_ids"""
