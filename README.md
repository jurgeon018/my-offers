# my-offers
МКС: мои объявления для агента

CURL поискового запроса:
```
curl -X POST \
  http://localhost:8000/v1/get-offers/ \
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
