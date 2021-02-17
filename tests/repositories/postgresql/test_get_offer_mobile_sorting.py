from my_offers import enums
from my_offers.repositories.postgresql.object_model import OFFER_TABLE, _prepare_sort_mobile_order


async def test_delete_offers_duplicates(mocker):
    # arrange

    # act
    update_date = _prepare_sort_mobile_order(enums.MobOffersSortType.update_date)
    move_to_archive_date = _prepare_sort_mobile_order(enums.MobOffersSortType.move_to_archive_date)
    price_asc = _prepare_sort_mobile_order(enums.MobOffersSortType.move_to_archive_date)
    price_desc = _prepare_sort_mobile_order(enums.MobOffersSortType.move_to_archive_date)

    # assert
    assert update_date[1] == OFFER_TABLE.offer_id
    assert move_to_archive_date[1] == OFFER_TABLE.offer_id
    assert price_asc[1] == OFFER_TABLE.offer_id
    assert price_desc[1] == OFFER_TABLE.offer_id
