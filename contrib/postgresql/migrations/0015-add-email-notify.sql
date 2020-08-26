CREATE TABLE offers_email_notification_settings
(
    user_id         bigint not null primary key,
    subscription_id text   not null,
    email           text   not null
);

DROP INDEX offers_duplicate_notification_offer_id_duplicate_offer_id_idx;

CREATE TYPE notification_type as enum (
    'mobilePush',
    'emailPush'
    );
ALTER TABLE offers_duplicate_notification
    ADD COLUMN notification_type notification_type DEFAULT 'mobilePush' NOT NULL;

CREATE UNIQUE INDEX ON offers_duplicate_notification (offer_id, duplicate_offer_id, notification_type);
