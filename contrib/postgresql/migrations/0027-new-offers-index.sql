create index
    --concurrently
	on offers (master_user_id, status_tab, user_id, sort_date desc NULLS LAST, offer_id);
create index
    --concurrently
	on offers (master_user_id, status_tab, sort_date desc NULLS LAST, offer_id);
