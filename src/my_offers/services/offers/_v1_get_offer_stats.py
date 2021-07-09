import asyncio
from dataclasses import fields
from typing import Dict, Optional

from cian_core.degradation import DegradationResult, get_degradation_handler

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
from my_offers.services.favorites import get_favorites_counts_degradation_handler


async def v1_get_offer_stats_public(
        request: entities.GetOfferStatsV1Request,
        realty_user_id: int,
) -> entities.GetOfferStatsV1Response:
    (
        my_offer_stats_degradation_result,
        user_calls_by_offers_totals_degradation_result,
        favorites_degradation_result,
    ) = await asyncio.gather(
        _cian_api_site_v1_get_my_offer_stats_degradation_handler(
            CianApiSiteV1GetMyOfferStats(
                id=request.offer_id,
                deal_type=request.deal_type,
                offer_type=request.offer_type,
            )
        ),
        _v1_get_user_calls_by_offers_totals_degradation_handler(
            GetUserCallsByOffersStatsRequest(
                user_id=realty_user_id,
                offer_ids=[request.offer_id],
            )
        ),
        get_favorites_counts_degradation_handler(
            offer_ids=[request.offer_id],
        ),
    )

    response = _get_response(my_offer_stats_degradation_result)

    _add_calls_to_response(
        request.offer_id,
        response,
        user_calls_by_offers_totals_degradation_result,
    )

    _add_favorites_to_response(
        request.offer_id,
        response,
        favorites_degradation_result,
    )

    return response


def _add_favorites_to_response(
        offer_id: int,
        response: entities.GetOfferStatsV1Response,
        degradation_result: DegradationResult,
) -> None:
    result: Dict[int, int] = degradation_result.value

    for field in fields(StatsData):
        setattr(
            getattr(response.data, field.name),
            'favorites_total',
            result.get(offer_id)
        )


def _add_calls_to_response(
        offer_id: int,
        response: entities.GetOfferStatsV1Response,
        degradation_result: DegradationResult,
) -> None:
    result: GetUserCallsByOffersTotalsResponse = degradation_result.value

    offer_calls = {
        offer_call.offer_id: offer_call
        for offer_call in result.data
    }

    for field in fields(StatsData):
        setattr(
            getattr(response.data, field.name),
            'calls_total',
            offer_calls.get(offer_id) and offer_calls.get(offer_id).calls_count
        )


def _get_response(degradation_result: DegradationResult) -> entities.GetOfferStatsV1Response:
    result: GetMyOfferStatsResponse = degradation_result.value
    data: MyOffersStatsGetMyOfferStatsResponse = result.data

    stats_data = {
        field.name: _get_period_stats(getattr(data, field.name))
        for field in fields(StatsData)
    }

    return entities.GetOfferStatsV1Response(
        data=StatsData(**stats_data),
        emergency_message=None,
    )


def _get_period_stats(data: Optional[MonolithPeriodStats]) -> PeriodStats:
    if data is None:
        return PeriodStats()

    return PeriodStats(
        coverage=data.coverage,
        favorites_total=data.favorites,
        offer_show=data.offer_show,
        offer_show_total=data.offer_show_total,
        phone_show=data.phone_show,
        search_results_show=data.search_results_show,
        search_results_selected_chart=data.search_results_selected_chart,
        search_results_show_chart=data.search_results_show_chart,
        show_chart=data.show_chart,
        calls_total=None,
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
