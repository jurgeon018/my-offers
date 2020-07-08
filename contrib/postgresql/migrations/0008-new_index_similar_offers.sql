DROP INDEX /*CONCURRENTLY*/ offers_house_id_idx;
DROP INDEX /*CONCURRENTLY*/ offers_district_id_idx;

CREATE INDEX /*CONCURRENTLY*/ ON offers (house_id, price)
    WHERE house_id is not null and status_tab='active';

CREATE INDEX /*CONCURRENTLY*/ ON offers (district_id, deal_type, price)
    WHERE district_id is not null and status_tab='active';