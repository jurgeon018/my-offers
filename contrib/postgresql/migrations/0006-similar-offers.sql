ALTER TABLE offers
ADD COLUMN  district_id int,
ADD COLUMN  house_id int;

CREATE INDEX CONCURRENTLY ON offers (district_id) WHERE district_id is not null;
CREATE INDEX CONCURRENTLY ON offers (house_id) WHERE house_id is not null;