create table offers_duplicate_notification(
    offer_id bigint not null,
    duplicate_offer_id bigint not null,
    send_at timestamp with time zone not null
);

create unique index on offers_duplicate_notification(offer_id, duplicate_offer_id);
