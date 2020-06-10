from cian_enum import StrEnum


class NotActiveStatus(StrEnum):
    """Статус объявления во вкладке Неактивные"""
    premoderation = 'premoderation'
    """На премодерации"""
    import_error = 'import_error'
    """Ошибка импорта"""
    discontinued = 'discontinued'
    """Снято с публикации"""
