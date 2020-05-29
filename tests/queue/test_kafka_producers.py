import pytest

from my_offers.queue.kafka_producers import OfferDuplicateEventProducer
from my_offers.repositories.monolith_cian_announcementapi.entities import Geo, LocationPath


@pytest.mark.parametrize(
    ('geo', 'expected'),
    (
        (None, None),
        (Geo(location_path=LocationPath(child_to_parent=[1, 2, 3])), 3)
    )
)
def test_offer_duplicate_event_producer__get_region_id(geo, expected):
    # arrange & act
    result = OfferDuplicateEventProducer._get_region_id(geo)

    # assert
    assert result == expected
