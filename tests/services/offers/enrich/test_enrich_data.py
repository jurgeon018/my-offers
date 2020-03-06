from unittest import mock

import pytest

from my_offers import enums
from my_offers.entities.enrich import AddressUrlParams
from my_offers.repositories.monolith_cian_announcementapi.entities import AddressInfo, address_info
from my_offers.services.offers.enrich.enrich_data import AddressUrls, EnrichData, EnrichParams


def test_get_geo_url_params(mocker):
    # arrange
    params = EnrichParams()
    params.add_geo_url_id(
        deal_type=enums.DealType.rent,
        offer_type=enums.OfferType.flat,
        geo_type=address_info.Type.underground,
        geo_id=11
    )

    expected = [
        AddressUrlParams(
            deal_type=enums.DealType.rent,
            offer_type=enums.OfferType.flat,
            address_info=[
                AddressInfo(
                    id=11,
                    type=address_info.Type.underground
                )
            ]
        )
    ]

    # act
    result = params.get_geo_url_params()

    # assert
    assert result == expected


def test_address_urls__none__none(mocker):
    # arrange
    urls = AddressUrls()
    address = AddressInfo(id=11, type=address_info.Type.underground)

    # act
    result = urls.get_url(address)

    # assert
    assert result is None


def test_enrich_data__get_offer_offence__moderation_info_is_none(mocker):
    # arrange
    enrich_data = EnrichData(
        statistics={},
        auctions={},
        jk_urls={},
        geo_urls={},
        can_update_edit_dates={},
        import_errors={},
        moderation_info=None
    )

    # act
    result = enrich_data.get_offer_offence(offer_id=111)

    # assert
    assert result is None


@pytest.mark.parametrize('moderation_info, expected', [
    ({}, None),
    ({111: mock.sentinel.offer_offence}, mock.sentinel.offer_offence),
])
def test_enrich_data__get_offer_offence(mocker, moderation_info, expected):
    # arrange
    enrich_data = EnrichData(
        statistics={},
        auctions={},
        jk_urls={},
        geo_urls={},
        can_update_edit_dates={},
        import_errors={},
        moderation_info=moderation_info
    )

    # act
    result = enrich_data.get_offer_offence(offer_id=111)

    # assert
    assert result == expected
