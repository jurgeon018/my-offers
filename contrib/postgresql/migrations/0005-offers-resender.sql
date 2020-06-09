CREATE TABLE offers_resender_cron
(
    id          bigint,
--     session_id  text,
    row_version bigint,
    created_at  timestamp with time zone
);
