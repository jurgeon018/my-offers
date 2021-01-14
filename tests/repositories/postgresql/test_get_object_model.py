import pytest
from cian_test_utils import future

from my_offers.enums import GetOffersSortType
from my_offers.repositories.monolith_cian_announcementapi.entities import BargainTerms, ObjectModel, Phone
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Category
from my_offers.repositories.postgresql.object_model import get_object_model


PATH = 'my_offers.repositories.postgresql.object_model.'


@pytest.mark.gen_test
async def test_get_object_model(mocker):
    # arrange
    expected = ObjectModel(
        id=111,
        bargain_terms=BargainTerms(price=123),
        category=Category.flat_rent,
        phones=[Phone(country_code='1', number='12312')],
        cian_id=333,
    )
    get_object_models_mock = mocker.patch(f'{PATH}get_object_models', return_value=future(([expected], 1)))

    # act
    result = await get_object_model({'zz': 'yy'})

    # assert
    assert result == [expected]
    get_object_models_mock.assert_called_once_with(
        filters={'zz': 'yy'},
        limit=1,
        offset=0,
        sort_type=GetOffersSortType.by_default,
    )


@pytest.mark.gen_test
async def test_get_object_model__none__none(mocker):
    # arrange
    get_object_models_mock = mocker.patch(f'{PATH}get_object_models', return_value=future([]))

    # act
    result = await get_object_model({'zz': 'yy'})

    # assert
    assert result is None
    get_object_models_mock.assert_called_once_with(
        filters={'zz': 'yy'},
        limit=1,
        offset=0,
        sort_type=GetOffersSortType.by_default,
    )
