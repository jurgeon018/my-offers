from cian_enum import StrEnum


class OfferActionStatus(StrEnum):
    ok = 'ok'


class MassRestoreActionType(StrEnum):
    all = 'all'
    """Восстановить все объявления"""
    select = 'select'
    """Восстановить выбранные объявления"""
