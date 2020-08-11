alter table offers_similars_flat drop column offer_type;
alter table offers_similars_test drop column offer_type;

alter table offers_similars_flat alter column deal_type set not null;
alter table offers_similars_test alter column deal_type set not null;

alter table offers_similars_flat alter column sort_date set not null;
alter table offers_similars_test alter column sort_date set not null;
