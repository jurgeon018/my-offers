from cian_enum import NoFormat, StrEnum


class ChangePublisherStatus(StrEnum):
    """Статус смены владельца объявления"""

    __value_format__ = NoFormat
    in_progress = 'InProgress'
    """В обработке"""
    completed = 'Completed'
    """Завершено"""
    error = 'Error'
    """Завершено с ошибками"""
