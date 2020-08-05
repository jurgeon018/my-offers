create table if not exists offers_similar_flat
(
	offer_id bigint primary key,
	offer_type offer_type not null,
	group_id bigint,
	house_id integer,
	district_id integer,
	price double precision,
	rooms_count integer
);

create index on offers_similar_flat (group_id);
create index on offers_similar_flat (house_id, price);
create index on offers_similar_flat (district_id, price);

create table if not exists offers_similar_test
(
	offer_id bigint primary key,
	offer_type offer_type not null,
	group_id bigint,
	house_id integer,
	district_id integer,
	price double precision,
	rooms_count integer
);

create index on offers_similar_test (group_id);
create index on offers_similar_test (house_id, price);
create index on offers_similar_test (district_id, price);
