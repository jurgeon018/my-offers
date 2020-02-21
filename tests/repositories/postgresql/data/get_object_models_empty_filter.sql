SELECT offers.raw_data, count(*) OVER () AS total_count 
FROM offers ORDER BY offers.sort_date DESC NULLS LAST, offers.offer_id 
 LIMIT $1 OFFSET $2
