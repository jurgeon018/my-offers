create table if not exists views_current
(
	offer_id bigint,
	year int,
	month int,
	day int,
	views counter,
	primary key ((offer_id, year, month), day)
);

create table if not exists views_daily
(
	offer_id bigint,
	year int,
	month int,
	day int,
	views int,
	primary key ((offer_id, year, month), day)
);

create table views_total
(
	offer_id bigint,
	year int,
	month int,
	day int,
	views int,
	views_total int,
	primary key ((offer_id, year, month), day)
);
