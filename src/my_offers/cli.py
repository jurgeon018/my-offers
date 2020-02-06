import json
from datetime import timedelta
from functools import partial

import click
from cian_core.rabbitmq.consumer_cli import register_consumer
from cian_core.web import Application
from tornado.ioloop import IOLoop

from my_offers import setup
from my_offers.queue import consumers, queues, schemas
from my_offers.services.announcement import process_announcement
from my_offers.web.urls import urlpatterns


@click.group()
def cli() -> None:
    setup()


@cli.command()
@click.option('--debug', is_flag=True)
@click.option('--host', type=str, default='127.0.0.1')
@click.option('--port', type=int, default=8000)
def serve(debug: bool, host: str, port: int) -> None:
    app = Application(urlpatterns, debug=debug)
    app.start(host=host, port=port)


register_consumer(
    command=cli.command('process_announcement_consumer'),
    queue=queues.process_announcements_queue,
    callback=consumers.process_announcement_callback,
    schema_cls=schemas.RabbitMQAnnouncementMessageSchema,
    dead_queue_enabled=True,
    dead_queue_ttl=timedelta(seconds=60),
)


@cli.command()
def run_tests() -> None:
    data = """
{
    "isInHiddenBase": false,
    "isByHomeOwner": false,
    "cianUserId": 15054485,
    "floorNumber": 2,
    "phones": [
        {
            "countryCode": "+7",
            "number": "9989990000"
        }
    ],
    "isRentByParts": false,
    "rentByPartsDescription": null,
    "category": "flatRent",
    "publishTerms": {
        "terms": [
            {
                "services": [
                    "paid"
                ],
                "type": "dailyTermless",
                "days": 1
            }
        ],
        "autoprolong": true,
        "infinitePublishPeriod": true
    },
    "userId": 15054485,
    "publishedUserId": 15054485,
    "id": 165456265,
    "bargainTerms": {
        "clientFee": 70,
        "leaseTermType": "longTerm",
        "price": 150000.0,
        "currency": "rur",
        "deposit": 200000,
        "bargainAllowed": false,
        "agentFee": 70,
        "prepayMonths": 2,
        "paymentPeriod": "monthly",
        "priceType": "all",
        "includedOptions": [],
        "utilitiesTerms": {
            "includedInPrice": true,
            "price": 0.0,
            "flowMetersNotIncludedInPrice": null
        }
    },
    "description": "Тестовое объявление ЦИАН",
    "totalArea": 20.0,
    "specialty": {
        "additionalTypes": [],
        "types": []
    },
    "photos": [],
    "geo": {
        "countryId": 138,
        "undergrounds": [
            {
                "transportType": "walk",
                "name": "Первомайская",
                "lineColor": "03238B",
                "time": 6,
                "lineId": 1,
                "id": 89,
                "isDefault": true
            },
            {
                "transportType": "walk",
                "name": "Щелковская",
                "lineColor": "03238B",
                "time": 19,
                "lineId": 1,
                "id": 153
            },
            {
                "transportType": "walk",
                "name": "Измайловская",
                "lineColor": "03238B",
                "time": 28,
                "lineId": 1,
                "id": 41
            }
        ],
        "calculatedUndergrounds": [],
        "coordinates": {
            "lat": 55.731871,
            "lng": 37.782773
        },
        "highways": [],
        "railways": [
            {
                "id": 701,
                "directionIds": [
                    13
                ],
                "distance": 7.0,
                "time": 88,
                "name": "Электрозаводская",
                "travelType": "byFoot"
            },
            {
                "id": 701,
                "directionIds": [
                    13
                ],
                "distance": 8.0,
                "time": 12,
                "name": "Электрозаводская",
                "travelType": "byCar"
            },
            {
                "id": 711,
                "directionIds": [
                    13
                ],
                "distance": 8.0,
                "time": 107,
                "name": "Сортировочная",
                "travelType": "byFoot"
            },
            {
                "id": 711,
                "directionIds": [
                    13
                ],
                "distance": 11.0,
                "time": 15,
                "name": "Сортировочная",
                "travelType": "byCar"
            },
            {
                "id": 712,
                "directionIds": [
                    20
                ],
                "distance": 10.0,
                "time": 128,
                "name": "Яуза",
                "travelType": "byFoot"
            }
        ],
        "userInput": "Россия, Москва, 10-я Парковая улица, 20",
        "address": [
            {
                "name": "Москва",
                "id": 1,
                "locationTypeId": 1,
                "fullName": "Москва",
                "type": "location",
                "shortName": "Москва",
                "isFormingAddress": true
            },
            {
                "name": "1-й Институтский",
                "id": 57,
                "fullName": "1-й Институтский проезд",
                "type": "street",
                "shortName": "1-й Институтский проезд",
                "isFormingAddress": true
            },
            {
                "name": "3csss",
                "id": 1738749,
                "fullName": "3csss",
                "type": "house",
                "shortName": "3csss",
                "isFormingAddress": true
            }
        ],
        "district": [
            {
                "parentId": 7,
                "locationId": 1,
                "id": 57,
                "name": "Вешняки",
                "type": "raion"
            },
            {
                "locationId": 1,
                "id": 7,
                "name": "ВАО",
                "type": "okrug"
            }
        ],
        "locationPath": {
            "countryId": 138,
            "childToParent": [
                1
            ]
        }
    },
    "building": {
        "cargoLiftsCount": 1,
        "materialType": "monolith",
        "hasGarbageChute": true,
        "parking": {},
        "passengerLiftsCount": 1,
        "floorsCount": 19,
        "cranageTypes": [],
        "extinguishingSystemTypes": [],
        "liftTypes": [],
        "infrastructure": {},
        "totalArea": 20.0,
        "buildYear": 2009,
        "openingHours": {},
        "deadline": {}
    },
    "land": {},
    "cianId": 165456265,
    "electricity": {},
    "gas": {},
    "water": {},
    "drainage": {},
    "objectGuid": "6799e1c9-ec66-4852-b6d8-3b2b36795c41",
    "garage": {},
    "roomsCount": 2,
    "repairType": "cosmetic",
    "isApartments": false,
    "flatType": "rooms",
    "isPenthouse": false,
    "status": "Published",
    "flags": {
        "isArchived": false
    },
    "editDate": "2020-02-05T16:06:42.97",
    "version": 2,
    "source": "website",
    "videos": [],
    "rowVersion": 49734164400,
    "callTrackingProvider": null,
    "emlsId": null,
    "kp": null,
    "platform": {
        "type": "qaAutotests",
        "version": null
    },
    "creationDate": "2020-02-05T16:06:42.97",
    "homeOwner": null
}    
"""
    data = """
    {
    "isInHiddenBase": false,
    "cianUserId": 15057491,
    "floorNumber": 4,
    "phones": [
        {
            "countryCode": "+7",
            "number": "9254554670"
        },
        {
            "countryCode": "+7",
            "number": "4952780244"
        }
    ],
    "isRentByParts": false,
    "rentByPartsDescription": null,
    "category": "flatRent",
    "publishTerms": {
        "terms": [
            {
                "services": [
                    "top3"
                ],
                "type": "dailyTermless",
                "days": 1
            }
        ],
        "autoprolong": false,
        "infinitePublishPeriod": true
    },
    "hasInternet": true,
    "userId": 15057491,
    "publishedUserId": 15057491,
    "id": 165454434,
    "bargainTerms": {
        "clientFee": 0,
        "leaseTermType": "longTerm",
        "price": 70000.0,
        "currency": "rur",
        "deposit": 70000,
        "bargainAllowed": false,
        "agentFee": 0,
        "prepayMonths": 1,
        "paymentPeriod": "monthly",
        "priceType": "all",
        "includedOptions": [],
        "utilitiesTerms": {
            "includedInPrice": true,
            "price": 0.0,
            "flowMetersNotIncludedInPrice": null
        }
    },
    "description": "ffff",
    "totalArea": 54.0,
    "specialty": {
        "additionalTypes": [],
        "types": []
    },
    "photos": [],
    "geo": {
        "countryId": 138,
        "undergrounds": [
            {
                "transportType": "walk",
                "name": "ЦСКА",
                "lineColor": "7ACDCE",
                "time": 10,
                "lineId": 27,
                "id": 352,
                "isDefault": true
            },
            {
                "transportType": "walk",
                "name": "Полежаевская",
                "lineColor": "94007C",
                "time": 18,
                "lineId": 11,
                "id": 97
            },
            {
                "transportType": "walk",
                "name": "Аэропорт",
                "lineColor": "00701A",
                "time": 20,
                "lineId": 3,
                "id": 9
            }
        ],
        "calculatedUndergrounds": [
            {
                "transportType": "walk",
                "time": 30,
                "distance": 2510,
                "id": 9
            },
            {
                "transportType": "transport",
                "time": 7,
                "distance": 4436,
                "id": 9
            }
        ],
        "coordinates": {
            "lat": 55.788581,
            "lng": 37.520734
        },
        "highways": [],
        "railways": [
            {
                "id": 699,
                "directionIds": [
                    11
                ],
                "distance": 3.0,
                "time": 6,
                "name": "Беговая",
                "travelType": "byCar"
            },
            {
                "id": 699,
                "directionIds": [
                    11
                ],
                "distance": 3.0,
                "time": 38,
                "name": "Беговая",
                "travelType": "byFoot"
            },
            {
                "id": 707,
                "directionIds": [
                    11
                ],
                "distance": 4.0,
                "time": 56,
                "name": "Тестовская",
                "travelType": "byFoot"
            },
            {
                "id": 707,
                "directionIds": [
                    11
                ],
                "distance": 6.0,
                "time": 12,
                "name": "Тестовская",
                "travelType": "byCar"
            },
            {
                "id": 694,
                "directionIds": [
                    11
                ],
                "distance": 5.0,
                "time": 9,
                "name": "Москва (Белорусский вокзал)",
                "travelType": "byCar"
            },
            {
                "id": 694,
                "directionIds": [
                    11
                ],
                "distance": 4.0,
                "time": 59,
                "name": "Москва (Белорусский вокзал)",
                "travelType": "byFoot"
            }
        ],
        "userInput": "г Москва, Ходынский б-р, д 19",
        "address": [
            {
                "name": "Москва",
                "id": 1,
                "locationTypeId": 1,
                "fullName": "Москва",
                "type": "location",
                "shortName": "Москва",
                "isFormingAddress": true
            },
            {
                "name": "Ходынский",
                "id": 3373,
                "fullName": "Ходынский бульвар",
                "type": "street",
                "shortName": "Ходынский бул.",
                "isFormingAddress": true
            },
            {
                "name": "19",
                "id": 1691399,
                "fullName": "19",
                "type": "house",
                "shortName": "19",
                "isFormingAddress": true
            }
        ],
        "district": [],
        "jk": {
            "house": {},
            "id": 1173,
            "name": "Гранд-парк"
        },
        "locationPath": {
            "countryId": 138,
            "childToParent": [
                1
            ]
        }
    },
    "building": {
        "cargoLiftsCount": 0,
        "materialType": "monolithBrick",
        "series": "Монолитный дом",
        "hasGarbageChute": true,
        "parking": {
            "type": "ground"
        },
        "passengerLiftsCount": 1,
        "floorsCount": 8,
        "ceilingHeight": 3.0,
        "cranageTypes": [],
        "extinguishingSystemTypes": [],
        "liftTypes": [],
        "infrastructure": {},
        "totalArea": 54.0,
        "buildYear": 2005,
        "openingHours": {},
        "deadline": {}
    },
    "land": {},
    "cianId": 165454434,
    "hasFurniture": true,
    "electricity": {},
    "gas": {},
    "water": {},
    "drainage": {},
    "objectGuid": "998f7df2-94bc-4a09-880b-2db6f0a5ed67",
    "garage": {},
    "roomsCount": 1,
    "hasKitchenFurniture": true,
    "hasTv": true,
    "hasWasher": true,
    "hasConditioner": true,
    "hasBathtub": true,
    "hasShower": false,
    "hasDishwasher": false,
    "repairType": "euro",
    "petsAllowed": false,
    "hasFridge": true,
    "childrenAllowed": true,
    "windowsViewType": "street",
    "kitchenArea": 20.0,
    "loggiasCount": 1,
    "balconiesCount": 0,
    "allRoomsArea": "25",
    "livingArea": 25.0,
    "separateWcsCount": 0,
    "flatType": "rooms",
    "isPenthouse": false,
    "combinedWcsCount": 1,
    "status": "Draft",
    "flags": {
        "isArchived": false,
        "draftReason": "import"
    },
    "editDate": "2020-02-06T14:47:50.59",
    "version": 2,
    "source": "upload",
    "videos": [],
    "rowVersion": 19734145143,
    "callTrackingProvider": null,
    "emlsId": null,
    "kp": null,
    "platform": {
        "type": "qaAutotests",
        "version": null
    },
    "creationDate": "2020-02-05T12:56:13.767",
    "homeOwner": null
}
    
    """
    IOLoop.current().run_sync(partial(process_announcement, json.loads(data)))
