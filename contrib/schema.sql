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
    'notActive',
    'declined',
    'archived',
    'deleted'
    );

create type offer_service as enum (
    'auction',
    'top3',
    'premium',
    'premium+highlight',
    'paid',
    'free'
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
    services          offer_service[]          not null,

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

CREATE TABLE offers_billing_contracts
(
    id                bigint                   not null primary key,
    user_id           bigint                   not null,
    actor_user_id     bigint                   not null,
    publisher_user_id bigint                   not null,
    offer_id          bigint                   not null,
    start_date        timestamp with time zone not null,
    payed_till        timestamp with time zone not null,
    row_version       bigint                   not null,
    is_deleted        boolean                  not null,
    created_at        timestamp with time zone not null,
    updated_at        timestamp with time zone not null
);
CREATE INDEX ON offers_billing_contracts (offer_id);

CREATE table offers_last_import_error
(
    offer_id   bigint                   not null primary key,
    type       varchar,
    message    varchar,
    created_at timestamp with time zone not null
);

CREATE TYPE offence_status as enum (
    'Confirmed',
    'Corrected',
    'Untruth'
    );

CREATE TABLE offers_offences
(
    offence_id     bigint primary key       not null,
    created_by     bigint                   not null,
    offer_id       bigint                   not null,
    offence_type   bigint                   not null,
    offence_status offence_status           not null,
    offence_text   text                     not null,
    row_version    bigint                   not null,
    created_date   timestamp with time zone not null,
    created_at     timestamp with time zone not null,
    updated_at     timestamp with time zone not null
);

CREATE INDEX ON offers_offences (offer_id);

create table offers_reindex_queue
(
    offer_id   bigint                   not null primary key,
    in_process bool                     not null default false,
    created_at timestamp with time zone not null
);
create index on offers_reindex_queue (created_at);
