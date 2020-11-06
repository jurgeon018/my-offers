from datetime import datetime

import pytest
from cian_test_utils import future
from simple_settings.utils import settings_stub

from my_offers import entities, enums
from my_offers.services.duplicates import update_offer_duplicates
from my_offers.services.duplicates._update_offer_duplicates import _check_duplicates_group


PATH = 'my_offers.services.duplicates._update_offer_duplicates.'


async def test_update_offers_duplicate_no_offers__return(mocker):
    # arrange
    get_offers_row_version_mock = mocker.patch(
        f'{PATH}get_offers_row_version',
        return_value=future()
    )

    # act
    await update_offer_duplicates(1)

    # arrange
    get_offers_row_version_mock.assert_called_once_with([1])


@pytest.mark.parametrize(
    ('similar', 'group', 'expected'),
    (
        (
            entities.OfferSimilar(
                offer_id=1,
                sort_date=datetime(2020, 8, 2),
                deal_type=enums.DealType.sale,
                district_id=1,
                house_id=10,
                price=100,
                rooms_count=2,
                group_id=None,
                old_price=None,
            ),
            [
                entities.OfferSimilar(
                    offer_id=10,
                    sort_date=datetime(2020, 8, 2),
                    deal_type=enums.DealType.sale,
                    district_id=1,
                    house_id=10,
                    price=100,
                    rooms_count=2,
                    group_id=2,
                    old_price=None,
                ),
            ],
            True,
        ),
        (
            None,
            [
                entities.OfferSimilar(
                    offer_id=10,
                    sort_date=datetime(2020, 8, 2),
                    deal_type=enums.DealType.sale,
                    district_id=1,
                    house_id=10,
                    price=100,
                    rooms_count=2,
                    group_id=2,
                    old_price=None,
                ),
            ],
            False,
        ),
        (
            entities.OfferSimilar(
                offer_id=1,
                sort_date=datetime(2020, 8, 2),
                deal_type=enums.DealType.sale,
                district_id=1,
                house_id=10,
                price=100,
                rooms_count=2,
                group_id=None,
                old_price=None,
            ),
            [
                entities.OfferSimilar(
                    offer_id=10,
                    sort_date=datetime(2020, 8, 2),
                    deal_type=enums.DealType.sale,
                    district_id=2,
                    house_id=10,
                    price=100,
                    rooms_count=2,
                    group_id=2,
                    old_price=None,
                ),
            ],
            False,
        ),
        (
            entities.OfferSimilar(
                offer_id=1,
                sort_date=datetime(2020, 8, 2),
                deal_type=enums.DealType.sale,
                district_id=1,
                house_id=10,
                price=100,
                rooms_count=2,
                group_id=None,
                old_price=None,
            ),
            [
                entities.OfferSimilar(
                    offer_id=10,
                    sort_date=datetime(2020, 8, 2),
                    deal_type=enums.DealType.sale,
                    district_id=1,
                    house_id=10,
                    price=130,
                    rooms_count=2,
                    group_id=2,
                    old_price=None,
                ),
            ],
            False,
        ),
        (
            entities.OfferSimilar(
                offer_id=1,
                sort_date=datetime(2020, 8, 2),
                deal_type=enums.DealType.sale,
                district_id=1,
                house_id=10,
                price=100,
                rooms_count=2,
                group_id=None,
                old_price=None,
            ),
            [
                entities.OfferSimilar(
                    offer_id=10,
                    sort_date=datetime(2020, 8, 2),
                    deal_type=enums.DealType.sale,
                    district_id=1,
                    house_id=10,
                    price=100,
                    rooms_count=5,
                    group_id=2,
                    old_price=None,
                ),
            ],
            False,
        ),
        (
            entities.OfferSimilar(
                offer_id=1,
                sort_date=datetime(2020, 8, 2),
                deal_type=enums.DealType.sale,
                district_id=1,
                house_id=10,
                price=100,
                rooms_count=None,
                group_id=None,
                old_price=None,
            ),
            [
                entities.OfferSimilar(
                    offer_id=10,
                    sort_date=datetime(2020, 8, 2),
                    deal_type=enums.DealType.sale,
                    district_id=1,
                    house_id=10,
                    price=100,
                    rooms_count=5,
                    group_id=None,
                    old_price=None,
                ),
            ],
            False,
        ),
    )
)
async def test__check_duplicates_group(mocker, similar, group, expected):
    # arrange
    get_offer_similar_mock = mocker.patch(
        f'{PATH}offers_similars.get_offer_similar',
        return_value=future(similar)
    )
    get_offers_similars_by_group_id_mock = mocker.patch(
        f'{PATH}offers_similars.get_offers_similars_by_group_id',
        return_value=future(group)
    )

    # act
    with settings_stub(DUPLICATE_CHECK_ENABLED=True):
        result = await _check_duplicates_group(offer_id=1, group_id=2)

    # arrange
    assert result == expected
    get_offer_similar_mock.assert_called_once_with(1)
    get_offers_similars_by_group_id_mock.assert_called_once_with(2)
