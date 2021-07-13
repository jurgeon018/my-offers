create table search_coverage.counters
(
	offer_id int,
	date date,
	searches_count counter,
	shows_count counter,
	primary key (offer_id, date)
)
with caching = {'keys': 'ALL', 'rows_per_partition': 'NONE'}
	and compaction = {'class': 'org.apache.cassandra.db.compaction.SizeTieredCompactionStrategy', 'max_threshold': '32', 'min_threshold': '4'}
	and compression = {'chunk_length_in_kb': '64', 'class': 'org.apache.cassandra.io.compress.LZ4Compressor'}
	and dclocal_read_repair_chance = 0.1;
