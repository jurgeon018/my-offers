SELECT offers.raw_data, count(*) OVER () AS total_count 
FROM offers 
WHERE offers.status_tab = $7 AND offers.deal_type = $1 AND offers.user_id = ANY (CAST($3 AS BIGINT[])) AND offers.has_photo = true AND offers.is_manual = false AND offers.is_in_hidden_base = false AND offers.master_user_id = $2 AND offers.services @> $6 AND to_tsvector($8, offers.search_text) @@ to_tsquery('russian', $9) ORDER BY offers.sort_date DESC NULLS LAST, offers.offer_id 
 LIMIT $4 OFFSET $5
