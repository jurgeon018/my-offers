from cian_enum import StrEnum


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
