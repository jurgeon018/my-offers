# my-offers
МКС: мои объявления для агента

CURL поискового запроса:
```
curl -X POST \
  http://localhost:8000/v2/get-offers/ \
  -H 'Content-Type: application/json' \
  -H 'Host: localhost:8000' \
  -d '{
	"userId": 12478339,
	"filters": {
		"statusTab": "active",
		"dealType": "sale",
		"offerType": "suburban",
		"services": ["paid"],
		"subAgentIds": [46610424],
		"hasPhoto": true,
		"isManual": false,
		"isInHiddenBase": false,
		"searchText": "+79112318015"
	},
	"pagination": {
		"limit": 50,
		"offset": 50
	}
}'
```

Переиндескация объявлений
1. Добавить объявления в очередь на переиндексацию
```
insert into offers_reindex_queue(offer_id, created_at)
select
    offer_id,
    current_timestamp
from
    offers
where
    services && '{"highlight"}'
;
```
2. запустить комманду `my-offers reindex-offers`
