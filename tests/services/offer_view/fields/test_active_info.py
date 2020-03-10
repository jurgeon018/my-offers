from my_offers.entities.get_offers import ActiveInfo
from my_offers.enums import OfferVas
from my_offers.repositories.monolith_cian_announcementapi.entities import PublishTerm, PublishTerms, TariffIdentificator
from my_offers.repositories.monolith_cian_announcementapi.entities.publish_term import Services, Type
from my_offers.repositories.monolith_cian_announcementapi.entities.tariff_identificator import TariffGridType
from my_offers.services.offer_view.fields import get_active_info


def test_get_active_info(mocker):
    # arrange
    publish_terms = PublishTerms(
        terms=[
            PublishTerm(
                days=14,
                type=Type.periodical,
                services=[Services.calltracking]
            ),
            PublishTerm(
                days=1,
                type=Type.daily_termless,
                services=[Services.paid],
                tariff_identificator=TariffIdentificator(
                    tariff_id=540401,
                    tariff_grid_type=TariffGridType.service_package_group,
                )
            )
        ],
        autoprolong=True,
        infinite_publish_period=True,
    )
    expected = ActiveInfo(
        vas=[OfferVas.payed],
        is_from_package=True,
        is_autoprolong=False,
        is_publication_time_ends=False,
        publish_features=[],
        auction=None,
    )

    # act
    result = get_active_info(publish_terms)

    # assert
    assert result == expected
