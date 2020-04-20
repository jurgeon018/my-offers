CREATE table offers_search_log(
    filters jsonb,
    found_cnt int,
    is_error bool,
    created_at timestamp with time zone not null default current_timestamp
);
