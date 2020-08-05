create table offers_similars_flat
(
	offer_id bigint primary key,
	offer_type offer_type not null,
	group_id bigint,
	house_id integer,
	district_id integer,
	price double precision,
	rooms_count integer
);

create index on offers_similars_flat (group_id);
create index on offers_similars_flat (house_id, price);
create index on offers_similars_flat (district_id, price);

create table offers_similars_test
(
	offer_id bigint primary key,
	offer_type offer_type not null,
	group_id bigint,
	house_id integer,
	district_id integer,
	price double precision,
	rooms_count integer
);

create index on offers_similars_test (group_id);
create index on offers_similars_test (house_id, price);
create index on offers_similars_test (district_id, price);
