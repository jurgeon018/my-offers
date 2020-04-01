from datetime import datetime, timedelta

import pytest
import pytz
from freezegun import freeze_time

from my_offers.entities.get_offers import ActiveInfo
from my_offers.enums import OfferVas
from my_offers.repositories.monolith_cian_announcementapi.entities import PublishTerm, PublishTerms, TariffIdentificator
from my_offers.repositories.monolith_cian_announcementapi.entities.publish_term import Services, Type
from my_offers.repositories.monolith_cian_announcementapi.entities.tariff_identificator import TariffGridType
from my_offers.services.offer_view.fields import get_active_info
from my_offers.services.offer_view.fields.active_info import _get_payed_remain


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
        is_publication_time_ends=False,
        publish_features=[],
        auction=None,
    )

    # act
    result = get_active_info(publish_terms=publish_terms, payed_till=None)

    # assert
    assert result == expected


@pytest.mark.parametrize(
    ('payed_till', 'expected'),
    (
        (None, None),
        (datetime(2020, 5, 10, tzinfo=pytz.utc), timedelta(days=38, seconds=43200)),
    )
)
@freeze_time('2020-04-01 12:00:00')
def test__get_payed_remain(payed_till, expected):
    # arrange

    # act
    result = _get_payed_remain(payed_till)

    # assert
    assert result == expected
