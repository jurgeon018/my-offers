CREATE TABLE offers_delete_queue
(
    offer_id   bigint                   not null primary key,
    delete_at  timestamp with time zone not null,
    created_at timestamp with time zone not null default current_timestamp
);
CREATE INDEX ON offers_delete_queue (delete_at);