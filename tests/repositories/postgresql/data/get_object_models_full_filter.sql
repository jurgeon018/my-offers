SELECT offers.raw_data, count(*) OVER () AS total_count 
FROM offers 
WHERE offers.status_tab = $8 AND offers.deal_type = $1 AND offers.offer_type = $3 AND offers.user_id = ANY (CAST($4 AS BIGINT[])) AND offers.has_photo = true AND offers.is_manual = false AND offers.is_in_hidden_base = false AND offers.master_user_id = $2 AND offers.services @> $7 AND to_tsvector($9, offers.search_text) @@ to_tsquery('russian', $10) ORDER BY offers.sort_date DESC NULLS LAST, offers.offer_id 
 LIMIT $5 OFFSET $6
