from datetime import date, datetime, timedelta

from cian_test_utils import future
from freezegun import freeze_time

from my_offers.services import statistics
from my_offers.services.statistics._cassandra_statistics._coverage import StatisticsCoverageRow
from my_offers.services.statistics._cassandra_statistics._views import ViewsRow


async def test_get_favorites_counts(mocker):
    # arrange
    now = datetime(2020, 4, 29)
    completed_date = datetime(2020, 4, 20)
    offer_ids = [1, 2, 3]
    coverage_total = [
        StatisticsCoverageRow(offer_id=1, favorite_added=10, searches_count=0)
    ]
    coverage_current = [
        StatisticsCoverageRow(offer_id=2, favorite_added=20, searches_count=0),
        StatisticsCoverageRow(offer_id=2, favorite_added=15, searches_count=0),
    ]

    mocker.patch(
        'my_offers.services.statistics._statistics.base_cs_repo.get_completed_date',
        return_value=future(completed_date)
    )
    get_offers_coverage_total = mocker.patch(
        'my_offers.services.statistics._statistics.coverage_cs_repo.get_offers_coverage_total',
        return_value=future(coverage_total)
    )
    get_offers_coverage_current = mocker.patch(
        'my_offers.services.statistics._statistics.coverage_cs_repo.get_offers_coverage_current',
        return_value=future(coverage_current)
    )

    # act
    with freeze_time(now):
        result = await statistics.get_favorites_counts(offer_ids=offer_ids)

    # assert
    assert result == {
        1: 10,
        2: 35,
        3: 0
    }
    get_offers_coverage_total.assert_called_once_with(
        offers_ids=offer_ids,
        date_from=completed_date.date(),
        date_to=completed_date.date()
    )
    get_offers_coverage_current.assert_called_once_with(
        offers_ids=offer_ids,
        date_from=date(2020, 4, 21),
        date_to=now.date()
    )


async def test_get_favorites_counts__not_coverage_data(mocker):
    # arrange
    now = datetime(2020, 4, 29)
    completed_date = datetime(2020, 4, 20)
    offer_ids = [1, 2, 3]

    mocker.patch(
        'my_offers.services.statistics._statistics.base_cs_repo.get_completed_date',
        return_value=future(completed_date)
    )
    get_offers_coverage_total = mocker.patch(
        'my_offers.services.statistics._statistics.coverage_cs_repo.get_offers_coverage_total',
        return_value=future([])
    )
    get_offers_coverage_current = mocker.patch(
        'my_offers.services.statistics._statistics.coverage_cs_repo.get_offers_coverage_current',
        return_value=future([])
    )

    # act
    with freeze_time(now):
        result = await statistics.get_favorites_counts(offer_ids=offer_ids)

    # assert
    assert result == {
        1: 0,
        2: 0,
        3: 0
    }
    get_offers_coverage_total.assert_called_once_with(
        offers_ids=offer_ids,
        date_from=completed_date.date(),
        date_to=completed_date.date()
    )
    get_offers_coverage_current.assert_called_once_with(
        offers_ids=offer_ids,
        date_from=date(2020, 4, 21),
        date_to=now.date()
    )


async def test_get_searches_counts(mocker, fake_settings):
    # arrange
    offer_ids = [1, 2, 3]
    date_from = datetime(2020, 4, 10)
    date_to = datetime(2020, 4, 20)
    completed_date = datetime(2020, 4, 21)

    coverage_daily = [
        StatisticsCoverageRow(offer_id=1, favorite_added=0, searches_count=10)
    ]
    coverage_current = [
        StatisticsCoverageRow(offer_id=2, favorite_added=0, searches_count=20),
        StatisticsCoverageRow(offer_id=2, favorite_added=0, searches_count=15),
    ]

    await fake_settings.set(SEARCH_COVERAGE_NEW_TABLE_DATE_FROM=None)
    mocker.patch(
        'my_offers.services.statistics._statistics.base_cs_repo.get_completed_date',
        return_value=future(completed_date)
    )
    get_offers_coverage_daily = mocker.patch(
        'my_offers.services.statistics._statistics.coverage_cs_repo.get_offers_coverage_daily',
        return_value=future(coverage_daily)
    )
    get_offers_coverage_current = mocker.patch(
        'my_offers.services.statistics._statistics.coverage_cs_repo.get_offers_coverage_current',
        return_value=future(coverage_current)
    )

    # act
    result = await statistics.get_searches_counts(
        offer_ids=offer_ids,
        date_from=date_from,
        date_to=date_to
    )

    # assert
    assert result == {
        1: 10,
        2: 35,
        3: 0
    }
    get_offers_coverage_daily.assert_called_once_with(
        offers_ids=offer_ids,
        date_from=date_from.date(),
        date_to=completed_date.date()
    )
    get_offers_coverage_current.assert_called_once_with(
        offers_ids=offer_ids,
        date_from=(completed_date + timedelta(days=1)).date(),
        date_to=date_to.date()
    )


async def test_get_searches_counts__search_coverage_is_enabled(mocker, fake_settings):
    # arrange
    offer_ids = [1, 2, 3]
    date_from = datetime(2020, 4, 10)
    date_to = datetime(2020, 4, 20)
    completed_date = datetime(2020, 4, 21)
    new_table_date_from = datetime(2020, 4, 11).date()

    coverage_daily = [
        StatisticsCoverageRow(offer_id=1, favorite_added=0, searches_count=10)
    ]
    coverage_current = [
        StatisticsCoverageRow(offer_id=2, favorite_added=0, searches_count=20),
        StatisticsCoverageRow(offer_id=2, favorite_added=0, searches_count=15),
    ]
    coverage_counters = [
        StatisticsCoverageRow(offer_id=2, favorite_added=0, searches_count=7),
    ]

    await fake_settings.set(SEARCH_COVERAGE_NEW_TABLE_DATE_FROM=str(new_table_date_from))
    mocker.patch(
        'my_offers.services.statistics._statistics.base_cs_repo.get_completed_date',
        return_value=future(completed_date)
    )
    get_offers_coverage_daily = mocker.patch(
        'my_offers.services.statistics._statistics.coverage_cs_repo.get_offers_coverage_daily',
        return_value=future(coverage_daily)
    )
    get_offers_coverage_current = mocker.patch(
        'my_offers.services.statistics._statistics.coverage_cs_repo.get_offers_coverage_current',
        return_value=future(coverage_current)
    )
    get_offers_counters = mocker.patch(
        'my_offers.services.statistics._statistics.search_coverage_cs_repo.get_offers_counters',
        return_value=future(coverage_counters)
    )

    # act
    result = await statistics.get_searches_counts(
        offer_ids=offer_ids,
        date_from=date_from,
        date_to=date_to
    )

    # assert
    assert result == {
        1: 10,
        2: 7,
        3: 0
    }
    get_offers_coverage_daily.assert_called_once_with(
        offers_ids=offer_ids,
        date_from=date_from.date(),
        date_to=completed_date.date()
    )
    get_offers_coverage_current.assert_called_once_with(
        offers_ids=offer_ids,
        date_from=(completed_date + timedelta(days=1)).date(),
        date_to=date_to.date()
    )
    get_offers_counters.assert_called_once_with(
        offers_ids=offer_ids,
        date_from=new_table_date_from,
        date_to=date_to.date()
    )


async def test_get_views_counts(mocker):
    # arrange
    offer_ids = [1, 2, 3]
    date_from = datetime(2020, 4, 10)
    date_to = datetime(2020, 4, 27)
    completed_date = datetime(2020, 4, 21)

    views_daily_1 = [
        ViewsRow(offer_id=1, views=12),
        ViewsRow(offer_id=1, views=5),
    ]
    views_current_1 = [
        ViewsRow(offer_id=1, views=23)
    ]
    views_daily_2 = [
        ViewsRow(offer_id=2, views=1),
        ViewsRow(offer_id=2, views=5),
    ]
    views_current_2 = [
        ViewsRow(offer_id=2, views=3)
    ]
    views_daily_3 = [
        ViewsRow(offer_id=3, views=1),
        ViewsRow(offer_id=3, views=5),
    ]
    views_current_3 = [
        ViewsRow(offer_id=3, views=0),
        ViewsRow(offer_id=3, views=35),
    ]

    mocker.patch(
        'my_offers.services.statistics._statistics.base_cs_repo.get_completed_date',
        return_value=future(completed_date)
    )
    get_views_daily = mocker.patch(
        'my_offers.services.statistics._statistics.views_cs_repo.get_views_daily',
        side_effect=[
            future(views_daily_1),
            future(views_daily_2),
            future(views_daily_3),
        ]
    )
    get_views_current = mocker.patch(
        'my_offers.services.statistics._statistics.views_cs_repo.get_views_current',
        side_effect=[
            future(views_current_1),
            future(views_current_2),
            future(views_current_3),
        ]
    )

    # act
    result = await statistics.get_views_counts(
        offer_ids=offer_ids,
        date_from=date_from,
        date_to=date_to
    )

    # assert
    assert result == {
        1: 40,
        2: 9,
        3: 41
    }
    get_views_daily.assert_has_calls([
        mocker.call(day_from=10, day_to=21, month=4, offer_id=1, year=2020),
        mocker.call(day_from=10, day_to=21, month=4, offer_id=2, year=2020),
        mocker.call(day_from=10, day_to=21, month=4, offer_id=3, year=2020)
    ])
    get_views_current.assert_has_calls([
        mocker.call(day_from=22, day_to=27, month=4, offer_id=1, year=2020),
        mocker.call(day_from=22, day_to=27, month=4, offer_id=2, year=2020),
        mocker.call(day_from=22, day_to=27, month=4, offer_id=3, year=2020)
    ])


async def test_get_views_counts__current_view_delta_is_null(mocker):
    # arrange
    offer_ids = [1, 2, 3]
    date_from = datetime(2020, 4, 10)
    date_to = datetime(2020, 4, 27)
    completed_date = datetime(2020, 4, 30)

    views_daily_1 = [
        ViewsRow(offer_id=1, views=12),
        ViewsRow(offer_id=1, views=5),
    ]
    views_current_1 = [
        ViewsRow(offer_id=1, views=23)
    ]
    views_daily_2 = [
        ViewsRow(offer_id=2, views=1),
        ViewsRow(offer_id=2, views=5),
    ]
    views_current_2 = [
        ViewsRow(offer_id=2, views=3)
    ]
    views_daily_3 = [
        ViewsRow(offer_id=3, views=1),
        ViewsRow(offer_id=3, views=3),
    ]
    views_current_3 = [
        ViewsRow(offer_id=3, views=0),
        ViewsRow(offer_id=3, views=35),
    ]

    mocker.patch(
        'my_offers.services.statistics._statistics.base_cs_repo.get_completed_date',
        return_value=future(completed_date)
    )
    get_views_daily = mocker.patch(
        'my_offers.services.statistics._statistics.views_cs_repo.get_views_daily',
        side_effect=[
            future(views_daily_1),
            future(views_daily_2),
            future(views_daily_3),
        ]
    )
    get_views_current = mocker.patch(
        'my_offers.services.statistics._statistics.views_cs_repo.get_views_current',
        side_effect=[
            future(views_current_1),
            future(views_current_2),
            future(views_current_3),
        ]
    )

    # act
    result = await statistics.get_views_counts(
        offer_ids=offer_ids,
        date_from=date_from,
        date_to=date_to
    )

    # assert
    assert result == {
        1: 17,
        2: 6,
        3: 4
    }
    get_views_daily.assert_has_calls([
        mocker.call(day_from=10, day_to=30, month=4, offer_id=1, year=2020),
        mocker.call(day_from=10, day_to=30, month=4, offer_id=2, year=2020),
        mocker.call(day_from=10, day_to=30, month=4, offer_id=3, year=2020)
    ])
    get_views_current.assert_not_called()
