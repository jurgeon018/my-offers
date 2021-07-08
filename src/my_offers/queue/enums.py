from cian_enum import StrEnum, UpperCamelCaseFormat


class PushType(StrEnum):
    push_offer_duplicate = 'push_offer_duplicate'
    """появилась объявка на дубль"""
    push_price_change_offer_duplicate = 'push_price_change_offer_duplicate'
    """изменение цены на объявку-дубль"""


class OfferRelevanceCheckStatusId(StrEnum):
    relevance_confirmation_required = 'relevance_confirmation_required'
    """Ожидает подтверждения актуальности"""


class OfferRelevanceTypeMessage(StrEnum):
    warning_only = 'warning_only'
    """Плашка без даты отклонения"""
    without_message = 'without_message'
    """Без плашки"""


class AgentRelationState(StrEnum):
    __value_format__ = UpperCamelCaseFormat

    request = 'Request'
    """Отправлена заявка на добавление агента к агентству"""
    active = 'Active'
    """Активный агент"""
    processing = 'Processing'
    """Агент в процессе активации / блокировки"""
    blocked = 'Blocked'
    """Заблокированный агент"""
    deleted = 'Deleted'
    """Удаленный агент"""
    deleted_and_hidden = 'DeletedAndHidden'
    """Удаленный и скрытый агент"""
