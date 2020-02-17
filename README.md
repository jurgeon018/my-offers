# my-offers
МКС: мои объявления для агента

CURL поискового запроса:
```
curl --location --request POST 'http://localhost:8000/v1/get-offers/' \
--header 'Content-Type: application/json' \
--data-raw '{
	"statusTab": "active",
	"userId": 12478339,
	"dealType": "sale",
	"offerType": "suburban",
	"services": ["paid"],
	"subAgentIds": [46610424],
	"hasPhoto": true,
	"isManual": false,
	"isInHiddenBase": false,
	"searchText": "+79112318015"
}'
```
