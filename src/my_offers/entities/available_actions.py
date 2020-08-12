from dataclasses import dataclass


@dataclass
class AvailableActions:
    can_edit: bool
    """Можно редактировать"""
    can_restore: bool
    """Можно восстановить"""
    can_update_edit_date: bool
    """Можно обновить дату"""
    can_move_to_archive: bool
    """Пользователь может перенести объявление в архив"""
    can_delete: bool
    """Можно ли удалить объялвение"""
    can_raise: bool
    """Можно ли поднять в размещении"""
    can_change_publisher: bool
    """Можно ли сменить владельца объявления"""
    can_view_similar_offers: bool
    """Может ли пользователь увидеть дубли/похожие"""
