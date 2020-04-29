create table offers_duplicates(
    offer_id bigint not null primary key,
    group_id bigint not null,
    created_at timestamp with time zone not null,
    updated_at timestamp with time zone
);

create index on offers_duplicates(group_id);
