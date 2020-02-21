from my_offers import enums
from my_offers.repositories.monolith_cian_announcementapi.entities import (
    AddressInfo,
    BargainTerms,
    Geo,
    Jk,
    ObjectModel,
    Phone,
    UndergroundInfo,
)
from my_offers.repositories.monolith_cian_announcementapi.entities.address_info import Type
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Category
from my_offers.services.offers.enrich.prepare_enrich_params import prepare_enrich_params


def test_prepare_enrich_params(mocker):
    # arrange
    models = [
        ObjectModel(
            id=111,
            bargain_terms=BargainTerms(price=123.0),
            geo=Geo(
                undergrounds=[UndergroundInfo(line_color='12321', name='Сокольники', is_default=True, id=33)],
                address=[AddressInfo(id=1, type=Type.location)],
                jk=Jk(id=555)
            ),
            category=Category.bed_rent,
            phones=[Phone(country_code='1', number='12312')],
        ),
    ]

    # act
    result = prepare_enrich_params(models)

    # assert
    assert result._jk_ids == {555}
    assert result._offer_ids == {111}
    assert result._geo_url_params == {
        (enums.DealType.rent, enums.OfferType.flat): {
            Type.location: {1: 1},
            Type.underground: {33: 33},
        }
    }
