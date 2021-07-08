create table views_current
(
	offer_id bigint,
	year int,
	month int,
	day int,
	views counter,
	primary key ((offer_id, year, month), day)
)
with caching = {'keys': 'ALL', 'rows_per_partition': 'NONE'}
	and compaction = {'class': 'org.apache.cassandra.db.compaction.SizeTieredCompactionStrategy', 'max_threshold': '32', 'min_threshold': '4'}
	and compression = {'chunk_length_in_kb': '64', 'class': 'org.apache.cassandra.io.compress.LZ4Compressor'}
	and dclocal_read_repair_chance = 0.1;

create table views_daily
(
	offer_id bigint,
	year int,
	month int,
	day int,
	views int,
	primary key ((offer_id, year, month), day)
)
with caching = {'keys': 'ALL', 'rows_per_partition': 'NONE'}
	and compaction = {'class': 'org.apache.cassandra.db.compaction.SizeTieredCompactionStrategy', 'max_threshold': '32', 'min_threshold': '4'}
	and compression = {'chunk_length_in_kb': '64', 'class': 'org.apache.cassandra.io.compress.LZ4Compressor'}
	and dclocal_read_repair_chance = 0.1
	and default_time_to_live = 2678400
	and gc_grace_seconds = 86400;

create table views_total
(
	offer_id bigint,
	year int,
	month int,
	day int,
	views int,
	views_total int,
	primary key ((offer_id, year, month), day)
)
with caching = {'keys': 'ALL', 'rows_per_partition': 'NONE'}
	and compaction = {'class': 'org.apache.cassandra.db.compaction.SizeTieredCompactionStrategy', 'max_threshold': '32', 'min_threshold': '4'}
	and compression = {'chunk_length_in_kb': '64', 'class': 'org.apache.cassandra.io.compress.LZ4Compressor'}
	and dclocal_read_repair_chance = 0.1
	and default_time_to_live = 15552000
	and gc_grace_seconds = 86400;

create table coverage_current
(
	offer_id bigint,
	date date,
	favorite_added counter,
	phone_shows counter,
	position counter,
	position_top3 counter,
	search_results_selected counter,
	search_results_shown counter,
	primary key (offer_id, date)
)
with caching = {'keys': 'ALL', 'rows_per_partition': 'NONE'}
	and compaction = {'class': 'org.apache.cassandra.db.compaction.SizeTieredCompactionStrategy', 'max_threshold': '32', 'min_threshold': '4'}
	and compression = {'chunk_length_in_kb': '64', 'class': 'org.apache.cassandra.io.compress.LZ4Compressor'}
	and dclocal_read_repair_chance = 0.1
	and gc_grace_seconds = 86400;

create table coverage_total_v2
(
	offer_id bigint,
	date date,
	favorite_added int,
	phone_shows int,
	position bigint,
	position_top3 bigint,
	search_results_selected int,
	search_results_shown int,
	primary key (offer_id, date)
)
with caching = {'keys': 'ALL', 'rows_per_partition': 'NONE'}
	and compaction = {'class': 'org.apache.cassandra.db.compaction.TimeWindowCompactionStrategy', 'compaction_window_size': '4', 'compaction_window_unit': 'HOURS', 'max_threshold': '32', 'min_threshold': '4'}
	and compression = {'chunk_length_in_kb': '64', 'class': 'org.apache.cassandra.io.compress.LZ4Compressor'}
	and dclocal_read_repair_chance = 0.0
	and default_time_to_live = 432000
	and gc_grace_seconds = 14400;

create table coverage_daily_v2
(
	offer_id bigint,
	date date,
	favorite_added int,
	phone_shows int,
	position bigint,
	position_top3 bigint,
	search_results_selected int,
	search_results_shown int,
	primary key (offer_id, date)
)
with caching = {'keys': 'ALL', 'rows_per_partition': 'NONE'}
	and compaction = {'class': 'org.apache.cassandra.db.compaction.TimeWindowCompactionStrategy', 'compaction_window_size': '4', 'compaction_window_unit': 'HOURS', 'max_threshold': '32', 'min_threshold': '4'}
	and compression = {'chunk_length_in_kb': '64', 'class': 'org.apache.cassandra.io.compress.LZ4Compressor'}
	and dclocal_read_repair_chance = 0.0
	and default_time_to_live = 3456000
	and gc_grace_seconds = 14400;

create table completed_total
(
	id int primary key,
	day int,
	month int,
	year int
)
with caching = {'keys': 'ALL', 'rows_per_partition': 'NONE'}
	and compaction = {'class': 'org.apache.cassandra.db.compaction.SizeTieredCompactionStrategy', 'max_threshold': '32', 'min_threshold': '4'}
	and compression = {'chunk_length_in_kb': '64', 'class': 'org.apache.cassandra.io.compress.LZ4Compressor'}
	and dclocal_read_repair_chance = 0.1;
