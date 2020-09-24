create type offer_billing_service_type as enum (
    'FreeObject',
    'DebitObject',
    'PremiumObject',
    'Top3',
    'calltracking',
    'SubscriptionForPackage',
    'StatusPro',
    'ServicePackageActivation',
    'Penalty',
    'OrderCancellation',
    'OrderTransfer',
    'TechSpend',
    'TechTransfer',
    'BonusPaymentExpiration',
    'auction',
    'demand',
    'demandPackage',
    'cplCalltracking'
);

ALTER TABLE offers_billing_contracts
    ADD COLUMN service_types offer_billing_service_type[] DEFAULT array[]::offer_billing_service_type[] NOT NULL;
