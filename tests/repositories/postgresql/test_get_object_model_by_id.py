import pytest
from cian_test_utils import future

from my_offers import pg
from my_offers.repositories.monolith_cian_announcementapi.entities import BargainTerms, ObjectModel, Phone
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Category
from my_offers.repositories.postgresql.object_model import get_object_model_by_id


@pytest.mark.gen_test
@pytest.mark.parametrize(
    ('row', 'expected'),
    (
        (None, None),
        (
            {'id': 1, 'raw_data': '{"zz": "yy"}'},
            ObjectModel(
                id=111,
                bargain_terms=BargainTerms(price=123),
                category=Category.flat_rent,
                phones=[Phone(country_code='1', number='12312')]
            )
        )
    )
)
async def test_get_object_model_by_id(mocker, row, expected):
    # arrange
    mocker.patch(
        'my_offers.repositories.postgresql.object_model.object_model_mapper.map_from',
        return_value=expected,
    )
    pg.get().fetchrow.return_value = future(row)

    # act
    result = await get_object_model_by_id(111)

    # assert
    assert result == expected
