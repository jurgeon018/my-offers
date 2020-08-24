create table offers_duplicate_email_notification
(
    user_id         bigint not null,
    subscription_id text   not null,
    email           text   not null
);

create table offers_email_notification_settings
(
    user_id    bigint  not null,
    is_enabled boolean not null
);