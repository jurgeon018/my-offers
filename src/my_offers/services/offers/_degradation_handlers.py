from cian_core.degradation import get_degradation_handler
from simple_settings import settings

from my_offers.entities import AgentHierarchyData, GetOffersCountersMobileResponse
from my_offers.entities.get_offers import OfferCounters
from my_offers.repositories import postgresql
from my_offers.repositories.auction import v1_get_announcements_info_for_mobile
from my_offers.repositories.callbook import v1_get_user_calls_by_offers_totals
from my_offers.repositories.moderation_checks_orchestrator import v1_check_users_need_identification
from my_offers.repositories.postgresql import get_object_models, get_offers_offence
from my_offers.repositories.postgresql.agents import get_agent_by_user_id, get_agent_hierarchy_data, get_agent_names
from my_offers.repositories.postgresql.billing import get_offers_payed_till_excluding_calltracking
from my_offers.repositories.postgresql.object_model import get_object_models_total_count
from my_offers.repositories.postgresql.offer import (
    get_offer_counters,
    get_offer_counters_mobile,
    get_offers_payed_by,
    get_offers_update_at,
)
from my_offers.repositories.postgresql.offer_import_error import get_last_import_errors
from my_offers.repositories.postgresql.offer_premoderation import get_offer_premoderations
from my_offers.services import statistics
from my_offers.services.deactivated_service.get_deactivated_services import get_deactivated_services_for_offers


get_object_models_degradation_handler = get_degradation_handler(
    func=get_object_models,
    key='psql.get_object_models',
    default=[],
)

get_object_models_total_count_degradation_handler = get_degradation_handler(
    func=get_object_models_total_count,
    key='psql.get_object_models_total_count',
    default=settings.OFFER_LIST_LIMIT,
)

get_offer_counters_degradation_handler = get_degradation_handler(
    func=get_offer_counters,
    key='psql.get_offer_counters',
    default=OfferCounters(
        active=None,
        not_active=None,
        declined=None,
        archived=None,
    ),
)

get_offer_counters_mobile_degradation_handler = get_degradation_handler(
    func=get_offer_counters_mobile,
    key='psql.get_offer_counters_mobile',
    default=GetOffersCountersMobileResponse(
        rent=None,
        sale=None,
        archived=None,
        inactive=None,
    )
)

get_offers_offence_degradation_handler = get_degradation_handler(
    func=get_offers_offence,
    key='psql.get_offers_offence',
    default=[],
)

get_last_import_errors_degradation_handler = get_degradation_handler(
    func=get_last_import_errors,
    key='psql.get_last_import_errors',
    default=dict(),
)

get_agent_names_degradation_handler = get_degradation_handler(
    func=get_agent_names,
    key='psql.get_agent_names',
    default=[],
)

get_agent_hierarchy_data_degradation_handler = get_degradation_handler(
    func=get_agent_hierarchy_data,
    key='psql.get_agent_hierarchy_data',
    default=AgentHierarchyData(
        is_master_agent=False,
        is_sub_agent=False,
    ),
)

get_agent_data_handler = get_degradation_handler(
    func=get_agent_by_user_id,
    key='psql.get_agent_by_user_id',
    default=None,
)

get_offer_premoderations_degradation_handler = get_degradation_handler(
    func=get_offer_premoderations,
    key='psql.get_offer_premoderations',
    default=[],
)

get_offers_update_at_degradation_handler = get_degradation_handler(
    func=get_offers_update_at,
    key='psql.get_offers_update_at',
    default=dict(),
)

get_offers_payed_till_excluding_calltracking_degradation_handler = get_degradation_handler(
    func=get_offers_payed_till_excluding_calltracking,
    key='psql.get_offers_payed_till_excluding_calltracking',
    default=dict(),
)

get_similars_counters_by_offer_ids_degradation_handler = get_degradation_handler(
    func=postgresql.get_similars_counters_by_offer_ids,
    key='psql.get_similars_counters_by_offer_ids',
    default=dict(),
)

get_offers_payed_by_degradation_handler = get_degradation_handler(
    func=get_offers_payed_by,
    key='psql.get_offers_payed_by',
    default=dict(),
)

get_views_counts_degradation_handler = get_degradation_handler(
    func=statistics.get_views_counts,
    key='cassandra.get_views_counts',
    default=dict(),
)

get_searches_counts_degradation_handler = get_degradation_handler(
    func=statistics.get_searches_counts,
    key='cassandra.get_searches_counts',
    default=dict(),
)

get_favorites_counts_degradation_handler = get_degradation_handler(
    func=statistics.get_favorites_counts,
    key='cassandra.get_favorites_counts',
    default=dict(),
)

get_calls_count_degradation_handler = get_degradation_handler(
    func=v1_get_user_calls_by_offers_totals,
    key='v1_get_user_calls_by_offers_totals',
    default=None,
)

get_auctions_mobile_degradation_handler = get_degradation_handler(
    func=v1_get_announcements_info_for_mobile,
    key='v1_get_announcements_info_for_mobile',
    default=dict(),
)

get_offers_with_pending_identification_handler = get_degradation_handler(
    func=v1_check_users_need_identification,
    key='v1_check_users_need_identification',
    default=set(),
)

get_deactivated_services_degradation_handler = get_degradation_handler(
    func=get_deactivated_services_for_offers,
    key='get_deactivated_services_for_offers',
    default=dict(),
)
