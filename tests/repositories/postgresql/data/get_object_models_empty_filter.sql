SELECT offers.raw_data, count(*) OVER () AS total_count 
FROM offers 
WHERE offers.master_user_id = offers.payed_by OR offers.payed_by IS NULL ORDER BY offers.sort_date DESC NULLS LAST, offers.offer_id 
 LIMIT $1 OFFSET $2