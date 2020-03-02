SET ROLE my_offers_admin;

drop table offers;
drop type deal_type;
drop type offer_type;
drop type offer_status;
drop type service;

create type deal_type as enum (
    'rent',
    'sale'
    );

create type offer_type as enum (
    'flat',
    'suburban',
    'commercial',
    'newobject'
    );

create type offer_status_tab as enum (
    'active',
    'not_active',
    'declined',
    'archived',
    'deleted'
    );

create type service as enum (
    'auction',
    'top3',
    'premium',
    'highlight',
    'paid',
    'free',
    'calltracking'
    );

CREATE TABLE offers
(
-- базовые поля
    offer_id          bigint                   not null primary key,
    master_user_id    bigint                   not null,

-- поля для фильтров
    user_id           bigint                   not null,
    deal_type         deal_type                not null,
    offer_type        offer_type               not null,
    status_tab        offer_status_tab         not null,
    services          service[]                not null,

    is_manual         bool                     not null,
    is_in_hidden_base bool                     not null,
    has_photo         bool                     not null,

-- поля для поиска
    search_text       text                     not null,

-- поля для сортировок
    price             float,
    price_per_meter   float,
    total_area        float,
    street_name       text,
    walking_time      float,
    sort_date         timestamp with time zone,

-- системные поля
    raw_data          jsonb                    not null,
    row_version       bigint                   not null,
    is_test           boolean,
    created_at        timestamp with time zone not null,
    updated_at        timestamp with time zone not null
);

CREATE INDEX ON offers USING gin (to_tsvector('russian', search_text));
CREATE INDEX ON offers (master_user_id, status_tab);
CREATE INDEX ON offers (updated_at);


create type target_object_type as enum (
    'announcement',
    'announcement_lite',
    'account',
    'account_subscription',
    'account_service_package',
    'penalty',
    'order_cancellation',
    'order_transfer',
    'tech_transfer',
    'tech_spend',
    'expired_bonus_wallet',
    'post_paid',
    'demand',
    'demand_package'
    );

CREATE TABLE offers_billing_contracts
(
    id                 bigint                   not null primary key,
    user_id            bigint                   not null,
    actor_user_id      bigint                   not null,
    publisher_user_id  bigint                   not null,
    target_object_id   bigint                   not null,
    target_object_type target_object_type       not null,
    start_date         timestamp with time zone not null,
    payed_till         timestamp with time zone not null,
    raw_data           text                     not null,
    row_version        bigint                   not null,
    is_deleted         boolean                  not null
);
