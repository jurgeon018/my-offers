create table users_reindex_queue
(
	user_id bigint not null primary key,
	in_process boolean default false not null,
	created_at timestamp with time zone not null
);

create index on users_reindex_queue(created_at);