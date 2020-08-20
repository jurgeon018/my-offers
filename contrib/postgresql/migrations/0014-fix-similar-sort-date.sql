update offers_similars_test f set
    sort_date = o.sort_date
from
    offers o
where
    f.sort_date <> o.sort_date
    and f.offer_id = o.offer_id
;

update offers_similars_flat f set
    sort_date = o.sort_date
from
    offers o
where
    f.sort_date <> o.sort_date
    and f.offer_id = o.offer_id
;