
delete from offers_row_versions;
alter table offers_row_versions add column status_tab offer_status_tab not null;
