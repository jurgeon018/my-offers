update offers_duplicates set updated_at = created_at where updated_at is null;
create index on offers_duplicates(updated_at);
