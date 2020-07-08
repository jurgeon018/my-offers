from cian_enum import NoFormat, StrEnum


class TargetObjectType(StrEnum):
    __value_format__ = NoFormat

    announcement = 'Announcement'
    """Объявление"""
    announcement_lite = 'AnnouncementLite'
    account = 'Account'
    account_subscription = 'AccountSubscription'
    account_service_package = 'AccountServicePackage'
    penalty = 'Penalty'
    """Штрафное списание"""
    order_cancellation = 'OrderCancellation'
    """Отмена пополнения"""
    order_transfer = 'OrderTransfer'
    """Перенос пополнения"""
    tech_transfer = 'TechTransfer'
    """Технический перевод"""
    tech_spend = 'TechSpend'
    """Техническое списание"""
    expired_bonus_wallet = 'ExpiredBonusWallet'
    """Истекший бонусный кошелек"""
    post_paid = 'PostPaid'
    """Постоплата за услугу"""
    demand = 'Demand'
    """Оплата заявки"""
    demand_package = 'DemandPackage'
    """Оплата пакета заявок"""
    cpl_calltracking = 'CplCalltracking'
    """CPL Колтрекинг"""
