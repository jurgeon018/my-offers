SELECT offers.raw_data 
FROM offers 
WHERE offers.status_tab = $6 AND offers.deal_type = $1 AND offers.user_id = ANY (CAST($3 AS BIGINT[])) AND offers.has_photo = true AND offers.is_manual = false AND offers.is_in_hidden_base = false AND offers.master_user_id = $2 AND offers.services @> $5 AND to_tsvector($7, offers.search_text) @@ to_tsquery('russian', $8) ORDER BY offers.sort_date DESC NULLS LAST, offers.offer_id 
 LIMIT $4
