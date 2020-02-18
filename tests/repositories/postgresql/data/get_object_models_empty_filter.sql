SELECT offers.raw_data 
FROM offers ORDER BY offers.sort_date DESC NULLS LAST, offers.offer_id 
 LIMIT $1
