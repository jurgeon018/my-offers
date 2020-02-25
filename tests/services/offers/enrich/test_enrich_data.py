from my_offers import enums
from my_offers.entities.enrich import AddressUrlParams
from my_offers.repositories.monolith_cian_announcementapi.entities import AddressInfo, address_info
from my_offers.services.offers.enrich.enrich_data import AddressUrls, EnrichParams


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
