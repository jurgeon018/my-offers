from cian_enum import NoFormat, StrEnum


class OfferServiceTypes(StrEnum):
    __value_format__ = NoFormat
    free_object = 'FreeObject'
    debit_object = 'DebitObject'
    premium_object = 'PremiumObject'
    top3 = 'Top3'
    highlight = 'Highlight'
    calltracking = 'calltracking'
    xml_import = 'XmlImport'
    subscription = 'SubscriptionForPackage'
    status_pro = 'StatusPro'
    service_package_activation = 'ServicePackageActivation'
    penalty = 'Penalty'
    order_cancellation = 'OrderCancellation'
    order_transfer = 'OrderTransfer'
    tech_spend = 'TechSpend'
    tech_transfer = 'TechTransfer'
    bonus_payment_expiration = 'BonusPaymentExpiration'
    auction = 'auction'
    demand = 'demand'
    demand_package = 'demandPackage'
    cpl_calltracking = 'cplCalltracking'
    dynamic = 'dynamic'
