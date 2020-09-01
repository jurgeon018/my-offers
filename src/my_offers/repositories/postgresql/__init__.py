from my_offers.repositories.postgresql.agents import get_master_user_id, is_master_agent, save_agent
from my_offers.repositories.postgresql.billing import save_offer_contract, set_offer_contract_is_deleted_status
from my_offers.repositories.postgresql.moderation import get_offers_offence, save_offer_offence
from my_offers.repositories.postgresql.object_model import (
    get_object_models,
    get_offers_by_ids,
    get_offers_by_ids_keep_order,
)
from my_offers.repositories.postgresql.offer import (
    get_offers_creation_date,
    get_offers_ids_by_tab,
    get_offers_row_version,
    save_offer,
    save_offer_archive,
    update_offer,
    update_offer_master_user_id,
)
from my_offers.repositories.postgresql.offer_import_error import delete_offer_import_error
from my_offers.repositories.postgresql.offers_duplicate_notification import (
    delete_offers_duplicate_notification,
    get_user_email,
    is_available_email_notification,
    save_offers_duplicate_notification,
)
from my_offers.repositories.postgresql.offers_duplicates import (
    delete_offers_duplicates,
    get_offer_duplicates,
    update_offers_duplicate,
    update_offers_duplicates,
)
from my_offers.repositories.postgresql.offers_resender import get_last_row_version, save_cron_session, save_cron_stats
from my_offers.repositories.postgresql.offers_similars import (
    get_similar_counter_by_offer_id,
    get_similars_by_offer_id,
    get_similars_counters_by_offer_ids,
)
