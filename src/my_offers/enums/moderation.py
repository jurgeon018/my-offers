from cian_enum import NoFormat, StrEnum


class ModerationOffenceStatus(StrEnum):
    """Статус нарушения"""
    __value_format__ = NoFormat

    confirmed = 'Confirmed'
    """Подтверждено"""
    corrected = 'Corrected'
    """Снято-исправлено"""
    untruth = 'Untruth'
    """Неподтверждено"""
