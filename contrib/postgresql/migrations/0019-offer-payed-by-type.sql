CREATE TYPE offer_payed_by_type as enum (
    'byMaster',
    'byAgent'
    );

ALTER TABLE offers
    ADD COLUMN payed_by offer_payed_by_type;
