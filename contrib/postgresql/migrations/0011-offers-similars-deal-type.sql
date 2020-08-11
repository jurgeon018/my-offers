alter table offers_similars_flat alter column offer_type drop not null;
alter table offers_similars_test alter column offer_type drop not null;

alter table offers_similars_flat add column deal_type deal_type;
alter table offers_similars_test add column deal_type deal_type;

alter table offers_similars_flat add column sort_date timestamp with time zone;
alter table offers_similars_test add column sort_date timestamp with time zone;