CREATE TABLE offer_relevance_warnings
(
    offer_id        bigint not null primary key,
    check_id        text   not null,
    active          bool   not null,
    due_date        timestamp with time zone,
    created_at      timestamp with time zone not null,
    updated_at      timestamp with time zone not null
);
