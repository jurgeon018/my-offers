import pytest

from my_offers import enums
from my_offers.repositories.postgresql.object_model import OFFER_TABLE, _prepare_sort_mobile_order


@pytest.mark.parametrize('sort_input', [
    enums.MobOffersSortType.update_date,
    enums.MobOffersSortType.move_to_archive_date,
    enums.MobOffersSortType.price_asc,
    enums.MobOffersSortType.price_desc,
])
async def test_prepare_sort_mobile_order(sort_input):
    # arrange

    # act
    sort_result = _prepare_sort_mobile_order(sort_input)

    # assert
    assert len(sort_result) == 2
    assert sort_result[1] == OFFER_TABLE.offer_id
