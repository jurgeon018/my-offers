create table if not exists views_current
(
	offer_id bigint,
	year int,
	month int,
	day int,
	views counter,
	primary key ((offer_id, year, month), day)
);
