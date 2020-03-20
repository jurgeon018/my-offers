from datetime import date

from cian_test_utils import future
from freezegun import freeze_time
from simple_settings.utils import settings_stub

from my_offers.entities import Coverage
from my_offers.repositories.search_coverage.entities import OfferCoverage, OffersCoverageRequest, OffersCoverageResponse
from my_offers.services.search_coverage._get_offers_search_coverage import get_offers_search_coverage


@freeze_time('2020-03-19')
async def test_get_offers_search_coverage(mocker):
    # arrange
    v1_get_offers_search_coverage_mock = mocker.patch(
        'my_offers.services.search_coverage._get_offers_search_coverage.v1_get_offers_search_coverage',
        return_value=future(
            OffersCoverageResponse(data=[OfferCoverage(offer_id=1, searches_count=10, coverage=20, shows_count=40)])
        )
    )

    request = OffersCoverageRequest(
        date_from=date(2020, 3, 17),
        date_to=date(2020, 3, 19),
        offer_ids=[1],
    )
    expected = {1: Coverage(searches_count=10, coverage=20, shows_count=40)}

    # act
    with settings_stub(DAYS_FOR_COVERAGE=2):
        result = await get_offers_search_coverage([1])

    # assert
    assert result == expected
    v1_get_offers_search_coverage_mock.assert_called_once_with(request)
