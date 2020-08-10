from my_offers.repositories.monolith_cian_announcementapi.entities import BargainTerms, ObjectModel, Phone, PublishTerms
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Category
from my_offers.services.similars._get_offer_similars import load_auction_bets


async def test_load_auction_bets__empty__empty():
    # arrange & act
    result = await load_auction_bets([])

    # assert
    assert result == {}


async def test_load_auction_bets__not_terms__empty():
    # arrange
    object_model = ObjectModel(
        id=111,
        bargain_terms=BargainTerms(price=123),
        category=Category.flat_rent,
        phones=[Phone(country_code='1', number='12312')],
        user_id=222,
        publish_terms=PublishTerms(autoprolong=True)
    )

    # act
    result = await load_auction_bets([object_model])

    # assert
    assert result == {}
