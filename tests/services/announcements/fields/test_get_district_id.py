import pytest

from my_offers.repositories.monolith_cian_announcementapi.entities import DistrictInfo
from my_offers.repositories.monolith_cian_announcementapi.entities.district_info import Type
from my_offers.services.similars.helpers.district import get_district_id


@pytest.mark.parametrize(
    ('district_info', 'expected'),
    (
        (None, None),
        (
            [
                DistrictInfo(
                    id=555,
                    name='Троицкое поселение',
                    type=Type.poselenie,
                    location_id=44,
                )
            ],
            555
        ),
        (
            [
                DistrictInfo(
                    id=326,
                    name='ТАО (Троицкий)',
                    type=Type.okrug,
                    location_id=1,
                ),
                DistrictInfo(
                    id=444,
                    name='Троицкий район',
                    type=Type.raion,
                    location_id=134,
                    parent_id=326
                )
            ],
            444
        ),
        (
            [
                DistrictInfo(
                    id=326,
                    name='ТАО (Троицкий)',
                    type=Type.okrug,
                    location_id=1,
                ),
                DistrictInfo(
                    id=488,
                    name='Троицкий микрорайон район',
                    type=Type.mikroraion,
                    location_id=1,
                    parent_id=326
                )
            ],
            488
        ),
        (
            [
                DistrictInfo(
                    id=326,
                    name='ТАО (Троицкий)',
                    type=Type.okrug,
                    location_id=1,
                ),
                DistrictInfo(
                    id=346,
                    name='Троицк',
                    type=Type.poselenie,
                    location_id=1,
                    parent_id=326
                )
            ],
            346
        ),
        (
            [
                DistrictInfo(
                    id=326,
                    name='ТАО (Троицкий)',
                    type=Type.okrug,
                    location_id=1,
                ),
                DistrictInfo(
                    id=444,
                    name='Троицкий район',
                    type=Type.raion,
                    location_id=134,
                    parent_id=326
                ),
                DistrictInfo(
                    id=488,
                    name='Троицкий микрорайон район',
                    type=Type.mikroraion,
                    location_id=1,
                    parent_id=444
                ),
                DistrictInfo(
                    id=526,
                    name='Троицк',
                    type=Type.poselenie,
                    location_id=1,
                    parent_id=488
                )
            ],
            526
        ),
        (
            [
                DistrictInfo(
                    id=133,
                    name='Центральный',
                    type=Type.raion,
                    location_id=2,
                ),
                DistrictInfo(
                    id=766,
                    name='Литейный',
                    type=Type.okrug,
                    location_id=2,
                    parent_id=133
                )
            ],
            766
        ),
        (
            [
                DistrictInfo(
                    id=133,
                    name='Центральный',
                    type=Type.raion,
                    location_id=2,
                ),
            ],
            133
        ),

    )
)
def test__get_district_id(district_info, expected):
    # arrange & act
    result = get_district_id(district_info)

    # assert
    assert result == expected
