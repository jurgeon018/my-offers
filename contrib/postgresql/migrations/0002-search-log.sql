CREATE table offers_search_log(
    user_id bigint,
    filters jsonb,
    found_cnt int,
    error text,
    created_at timestamp with time zone not null
);
