import pytest
from cian_entities import EntityMapper

from my_offers.repositories.monolith_cian_announcementapi.entities import Geo
from my_offers.services.announcement.fields.walking_time import get_walking_time
from tests.utils import load_json_data


geo_mapper = EntityMapper(Geo)


@pytest.mark.parametrize(
    ('geo', 'expected'),
    (
        (load_json_data(__file__, 'geo_calc_undergrounds.json'), 20),
        (load_json_data(__file__, 'geo_undergrounds.json'), 13),
        (load_json_data(__file__, 'geo_transport_undergrounds.json'), 130),
    ),
)
def test__get_walking_time(geo, expected):
    # arrange
    geo_obj = geo_mapper.map_from(geo)

    # act
    result = get_walking_time(geo_obj)

    # assert
    assert result == expected


def test__get_walking_time__none__none():
    # arrange & act
    result = get_walking_time(None)

    # assert
    assert result is None
