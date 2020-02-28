from cian_enum import StrEnum


class AnnouncementReportingV1RoutingKey(StrEnum):
    published = 'published'
    """Опубликован"""
    change = 'change'
    """Изменён"""
    blocked = 'blocked'
    """Заблокирован"""
    deactivated = 'deactivated'
    """Деактивирован"""
    draft = 'draft'
    """Черновик"""
    sold = 'sold'
    """Продан"""
    refused_by_moderator = 'refusedbymoderator'
    """Отклонен модератором"""
    removed_by_moderator = 'removedbymoderator'
    """Удален модератором"""
    deleted = 'deleted'
    """Удален"""
    move_to_archive = 'movetoarchive'
    """В архиве"""
    delete_permanently = 'deletepermanently'
    """Удален на всегда"""

    actualize_trust = 'actualizetrust'
    """Пересчет уровня доверия"""
    change_trust_for_builder = 'changetrustforbuilder'
    """Изменение Trust на тарифе застройщик"""
    image_changed = 'imagechanged'
    """Изменено изображение"""
    prolong = 'prolong'
    """Продление"""
    billed_after_published = 'billedafterpublished'
    """Тарификация после публикации"""
    accept_by_moderator = 'acceptbymoderator'
    """Проверка модератором объявления и его публикация"""

    # не обрабатываем
    # removed_from_archive = 'removed_from_archive'
    # """Удалено из архива"""
