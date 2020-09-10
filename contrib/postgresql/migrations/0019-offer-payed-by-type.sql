CREATE TYPE offer_payed_by_type as enum (
    'by_master',
    'by_agent'
    );

ALTER TABLE offers
    ADD COLUMN payed_by offer_payed_by_type;
