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

create type offer_status as enum (
    'draft',
    'published',
    'deactivated',
    'refused',
    'deleted',
    'sold',
    'moderate',
    'moderate',
    'removed_by_moderator',
    'blocked'
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

CREATE table offers(
-- базовые поля
    offer_id bigint not null primary key,
    master_user_id bigint not null,

-- поля для фильтров
    user_id bigint not null,
    deal_type deal_type not null,
    offer_type offer_type not null,
    status offer_status not null,
    services service[] not null,

    is_manual bool not null,
    is_in_hidden_base bool not null,
    has_photo bool not null,

-- поля для поиска
    search_text text not null,

-- поля для сортировок
    price float,
    price_per_meter float,
    total_area float,
    street_name text,
    walking_time float,
    publish_date timestamp,
    moderation_date timestamp,

-- системные поля
    raw_data jsonb not null,
    row_version bigint not null,
    created_at timestamp with time zone not null,
    updated_at timestamp with time zone not null
);

CREATE INDEX ON offers USING gin (to_tsvector('russian', search_text));
create index on offers(master_user_id, status);
