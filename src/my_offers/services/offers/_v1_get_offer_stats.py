from dataclasses import dataclass, fields
from datetime import datetime, timedelta
from typing import Any, Awaitable, Dict, Optional

import pytz
from cian_core.degradation import get_degradation_handler
from tornado import gen

from my_offers import entities
from my_offers.entities.get_offer_stats import PeriodStats, StatsData
from my_offers.repositories.callbook import v1_get_user_calls_by_offers_totals
from my_offers.repositories.callbook.entities import (
    GetUserCallsByOffersStatsRequest,
    GetUserCallsByOffersTotalsResponse,
)
from my_offers.repositories.monolith_python import cian_api_site_v1_get_my_offer_stats
from my_offers.repositories.monolith_python.entities import (
    CianApiSiteV1GetMyOfferStats,
    GetMyOfferStatsResponse,
    MyOffersStatsGetMyOfferStatsResponse,
    PeriodStats as MonolithPeriodStats,
)
from my_offers.repositories.monolith_python.entities.get_my_offer_stats_response import Status
from my_offers.repositories.postgresql.offer import get_offer_by_id
from my_offers.services.favorites import get_favorites_counts_degradation_handler
from my_offers.services.offers._degradation_handlers import (
    get_searches_counts_degradation_handler,
    get_views_counts_degradation_handler,
)


async def v1_get_offer_stats_public(
        request: entities.GetOfferStatsV1Request,
        realty_user_id: int,
) -> entities.GetOfferStatsV1Response:
    loaded_stats_data = await _load_stats_data(request.offer_id, realty_user_id)
    prepared_stats_data = _prepare_stats_data(loaded_stats_data, request.offer_id)
    return _get_response(prepared_stats_data)


@dataclass
class _PeriodExtraStats:
    views_counts: Optional[int]
    searches_counts: Optional[int]
    favorites: Optional[int]
    calls: Optional[int]


@dataclass
class _ExtraStatsData:
    day10: _PeriodExtraStats
    month: _PeriodExtraStats


@dataclass
class _PreparedStatsData:
    data: MyOffersStatsGetMyOfferStatsResponse
    extra_data: _ExtraStatsData


def _prepare_stats_data(loaded_stats_data: Dict[str, Any], offer_id: int) -> _PreparedStatsData:
    return _PreparedStatsData(
        data=loaded_stats_data['monolith_stats'].value.data,
        extra_data=_prepare_extra_data(
            offer_id=offer_id,
            stats_data=loaded_stats_data['stats'],
            favorites_data=loaded_stats_data['favorites'].value,
            calls_data=_prepare_calls_data(loaded_stats_data['calls'].value),
        ),
    )


def _prepare_calls_data(response: GetUserCallsByOffersTotalsResponse) -> Dict[int, int]:
    return {
        offer_call.offer_id: offer_call.calls_count
        for offer_call in response.data
    }


def _prepare_extra_data(
        offer_id: int,
        stats_data: Dict[str, Any],
        favorites_data: Dict[int, int],
        calls_data: Dict[int, int],
) -> _ExtraStatsData:
    # эти данные не меняются при изменении периода
    favorites = favorites_data.get(offer_id)
    calls = calls_data.get(offer_id)
    # endblock

    return _ExtraStatsData(
        day10=_PeriodExtraStats(
            views_counts=stats_data['views_counts_day10'].value.get(offer_id),
            searches_counts=stats_data['searches_counts_day10'].value.get(offer_id),
            favorites=favorites,
            calls=calls,
        ),
        month=_PeriodExtraStats(
            views_counts=stats_data['views_counts_month'].value.get(offer_id),
            searches_counts=stats_data['searches_counts_month'].value.get(offer_id),
            favorites=favorites,
            calls=calls,
        ),
    )


def _get_response(prepared_stats_data: _PreparedStatsData) -> entities.GetOfferStatsV1Response:
    data = prepared_stats_data.data
    extra_data = prepared_stats_data.extra_data

    stats_data = {
        period.name: _get_period_stats(
            period_data=getattr(data, period.name),
            period_extra_data=getattr(extra_data, period.name),
        )
        for period in fields(StatsData)
    }

    return entities.GetOfferStatsV1Response(
        data=StatsData(**stats_data),
        emergency_message=None,
    )


def _load_stats_data(offer_id: int, user_id: int) -> Awaitable[Dict[str, Any]]:
    return gen.multi({
        'monolith_stats': _load_monolith_stats(offer_id),
        'stats': _load_stats(offer_id),
        'favorites': _load_favorites(offer_id),
        'calls': _load_calls(offer_id, user_id),
    })


async def _load_favorites(offer_id: int):
    return await get_favorites_counts_degradation_handler(
        offer_ids=[offer_id],
    )


async def _load_calls(offer_id: int, user_id: int):
    return await _v1_get_user_calls_by_offers_totals_degradation_handler(
        GetUserCallsByOffersStatsRequest(
            user_id=user_id,
            offer_ids=[offer_id],
        )
    )


def _load_stats(offer_id: int) -> Awaitable[Dict[str, Any]]:
    date_to = datetime.now(tz=pytz.utc)
    date_from_10 = date_to - timedelta(days=10)
    date_from_30 = date_to - timedelta(days=30)

    return gen.multi({
        'views_counts_day10': get_views_counts_degradation_handler(
            offer_ids=[offer_id],
            date_from=date_from_10,
            date_to=date_to
        ),
        'views_counts_month': get_views_counts_degradation_handler(
            offer_ids=[offer_id],
            date_from=date_from_30,
            date_to=date_to
        ),
        'searches_counts_day10': get_searches_counts_degradation_handler(
            offer_ids=[offer_id],
            date_from=date_from_10,
            date_to=date_to
        ),
        'searches_counts_month': get_searches_counts_degradation_handler(
            offer_ids=[offer_id],
            date_from=date_from_30,
            date_to=date_to
        ),
    })


async def _load_monolith_stats(offer_id: int):
    offer = await get_offer_by_id(offer_id)
    return await _cian_api_site_v1_get_my_offer_stats_degradation_handler(
        CianApiSiteV1GetMyOfferStats(
            id=offer_id,
            deal_type=offer.deal_type,
            offer_type=offer.offer_type,
        )
    )


def _get_period_stats(
        period_data: Optional[MonolithPeriodStats],
        period_extra_data: _PeriodExtraStats,
) -> PeriodStats:
    if period_data is None:
        period_data = PeriodStats()

    return PeriodStats(
        coverage=period_data.coverage,
        favorites_total=period_extra_data.favorites or period_data.favorites,
        offer_show=period_extra_data.views_counts or period_data.offer_show,
        offer_show_total=period_data.offer_show_total,
        phone_show=period_data.phone_show,
        search_results_show=period_extra_data.searches_counts or period_data.search_results_show,
        search_results_selected_chart=period_data.search_results_selected_chart,
        search_results_show_chart=period_data.search_results_show_chart,
        show_chart=period_data.show_chart,
        calls_total=period_extra_data.calls,
    )


_cian_api_site_v1_get_my_offer_stats_degradation_handler = get_degradation_handler(
    func=cian_api_site_v1_get_my_offer_stats,
    key='statistics.cian_api_site_v1_get_my_offer_stats',
    default=GetMyOfferStatsResponse(
        data=MyOffersStatsGetMyOfferStatsResponse(),
        status=Status.ok,
    ),
)

_v1_get_user_calls_by_offers_totals_degradation_handler = get_degradation_handler(
    func=v1_get_user_calls_by_offers_totals,
    key='statistics.v1_get_user_calls_by_offers_totals',
    default=GetUserCallsByOffersTotalsResponse(data=[]),
)
