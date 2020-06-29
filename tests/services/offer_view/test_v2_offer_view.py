import pytest

from my_offers.entities.available_actions import AvailableActions
from my_offers.entities.get_offers import ActiveInfo, GetOfferV2, PageSpecificInfo, Statistics
from my_offers.entities.offer_view_model import OfferGeo, PriceInfo
from my_offers.repositories.monolith_cian_announcementapi.entities import BargainTerms, ObjectModel, Phone
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Category, Status
from my_offers.services.offer_view import v2_build_offer_view
from my_offers.services.offers.enrich.enrich_data import EnrichData


@pytest.fixture(name='enrich_data_mock')
def enrich_data_fixture():
    return EnrichData(

        auctions={},
        jk_urls={},
        geo_urls={},
        can_update_edit_dates={},
        import_errors={},
    )


def test_build_offer_view(enrich_data_mock):
    # arrange
    raw_offer = ObjectModel(
        id=111,
        status=Status.published,
        bargain_terms=BargainTerms(price=123),
        category=Category.flat_rent,
        phones=[Phone(country_code='1', number='12312')]
    )
    expected_result = GetOfferV2(
        id=111,
        main_photo_url=None,
        title='',
        url='https://cian.ru/rent/flat/111',
        geo=OfferGeo(address=None, newbuilding=None, underground=None),
        subagent=None,
        price_info=PriceInfo(exact=None, range=None),
        features=[],
        is_manual=True,
        created_at=None,
        display_date=None,
        archived_at=None,
        status='Опубликовано',
        statistics=Statistics(shows=None, views=None, favorites=None),
        available_actions=AvailableActions(
            can_edit=True,
            can_restore=True,
            can_update_edit_date=False,
            can_move_to_archive=True,
            can_delete=True,
            can_raise=True,
        ),
        page_specific_info=PageSpecificInfo(
            active_info=ActiveInfo(
                vas=[],
                is_from_package=False,
                is_publication_time_ends=False,
                publish_features=[],
                auction=None,
                payed_till=None,
            ),
            not_active_info=None,
            declined_info=None
        ),
        status_type=None
    )

    # act
    result = v2_build_offer_view(object_model=raw_offer, enrich_data=enrich_data_mock)

    # assert
    assert result == expected_result
