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

    district_id       int,
    house_id          int,

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
    updated_at        timestamp with time zone not null,
    event_date        timestamp with time zone not null
);

CREATE INDEX ON offers USING gin (to_tsvector('russian', search_text));
CREATE INDEX ON offers (master_user_id, status_tab);
CREATE INDEX ON offers (updated_at);
CREATE INDEX ON offers (house_id, price) WHERE house_id is not null and status_tab = 'active';
CREATE INDEX ON offers (district_id, deal_type, price) WHERE district_id is not null and status_tab = 'active';


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

CREATE TABLE offers_reindex_queue
(
    offer_id   bigint                   not null primary key,
    in_process bool                     not null default false,
    sync       bool                     not null default false,
    created_at timestamp with time zone not null
);
CREATE INDEX ON offers_reindex_queue (created_at);

CREATE TYPE account_type as enum (
    'Specialist',
    'Agency',
    'ManagementCompany',
    'RentDepartment'
    );

CREATE TABLE agents_hierarchy
(
    id                   bigint primary key       not null,
    row_version          bigint                   not null,
    account_type         account_type,
    realty_user_id       bigint                   not null,
    master_agent_user_id bigint,
    first_name           varchar,
    middle_name          varchar,
    last_name            varchar,
    created_at           timestamp with time zone not null,
    updated_at           timestamp with time zone not null
);
CREATE UNIQUE INDEX ON agents_hierarchy (realty_user_id);
CREATE INDEX ON agents_hierarchy (master_agent_user_id NULLS LAST);

create table offers_premoderations
(
    offer_id    bigint                   not null primary key,
    removed     boolean                  not null,
    row_version bigint                   not null,
    created_at  timestamp with time zone not null,
    updated_at  timestamp with time zone
);

CREATE INDEX ON offers_premoderations (offer_id, removed);

create table offers_duplicates
(
    offer_id   bigint                   not null primary key,
    group_id   bigint                   not null,
    created_at timestamp with time zone not null,
    updated_at timestamp with time zone
);

create index on offers_duplicates (group_id);

create table offers_duplicate_notification
(
    offer_id           bigint                   not null,
    duplicate_offer_id bigint                   not null,
    send_at            timestamp with time zone not null
);

create unique index on offers_duplicate_notification (offer_id, duplicate_offer_id, notification_type);

CREATE TABLE offers_resender_cron
(
    id           serial primary key,
    operation_id text                     not null,
    row_version  bigint                   not null,
    created_at   timestamp with time zone not null
);

CREATE TABLE offers_resender_stats
(
    operation_id         text                     not null,
    founded_from_elastic bigint                   not null,
    need_update          bigint                   not null,
    not_found_in_db      bigint                   not null,
    created_at           timestamp with time zone not null
);

create table offers_similars_flat
(
    offer_id    bigint primary key,
    deal_type   deal_type                not null,
    group_id    bigint,
    house_id    integer,
    district_id integer,
    price       double precision,
    rooms_count integer,
    sort_date   timestamp with time zone not null
);

create index offers_similars_flat_group_id_idx
    on offers_similars_flat (group_id);

create index offers_similars_flat_house_id_price_idx
    on offers_similars_flat (house_id, price);

create index offers_similars_flat_district_id_price_idx
    on offers_similars_flat (district_id, price);

create table offers_similars_test
(
    offer_id    bigint primary key,
    deal_type   deal_type                not null,
    group_id    bigint,
    house_id    integer,
    district_id integer,
    price       double precision,
    rooms_count integer,
    sort_date   timestamp with time zone not null
);


create index offers_similars_test_group_id_idx
    on offers_similars_test (group_id);

create index offers_similars_test_house_id_price_idx
    on offers_similars_test (house_id, price);

create index offers_similars_test_district_id_price_idx
    on offers_similars_test (district_id, price);


create table offers_duplicate_email_notification
(
    -- TODO: Запретить пользователю иметь больше одной подписки?
    user_id         bigint not null,
    subscription_id text   not null,
    email           text   not null
);

create table offers_email_notification_settings
(
    user_id    bigint  not null primary key,
    is_enabled boolean not null
);