ALTER TABLE offers
ADD COLUMN  district_id int,
ADD COLUMN  house_id int;

CREATE INDEX ON offers (district_id);