alter table offers_duplicates add column last_sync_date timestamp with time zone;
update offers_duplicates set last_sync_date = coalesce(updated_at, created_at);
alter table offers_duplicates alter column last_sync_date set not null;
create index on offers_duplicates(last_sync_date);
