from my_offers import enums
from my_offers.entities import get_offers
from my_offers.repositories.monolith_cian_announcementapi.entities import ObjectModel
from my_offers.services.offer_view.fields import get_active_info, get_not_active_info
from my_offers.services.offer_view.fields.declined_info import get_declined_info
from my_offers.services.offers.enrich.enrich_data import EnrichData


def get_page_specific_info(
        *,
        object_model: ObjectModel,
        enrich_data: EnrichData,
        status_tab: enums.OfferStatusTab,
) -> get_offers.PageSpecificInfo:
    result = get_offers.PageSpecificInfo()

    offer_id = object_model.id
    if status_tab.is_active:
        result.active_info = get_active_info(
            publish_terms=object_model.publish_terms,
            payed_till=enrich_data.get_payed_till(offer_id),
            duplicates_count=enrich_data.get_duplicates_counts(offer_id),
            same_building_count=enrich_data.get_same_building_counts(offer_id),
            offer_relevance_warning=enrich_data.get_offer_relevance_warning(offer_id),
        )
    elif status_tab.is_not_active:
        result.not_active_info = get_not_active_info(
            status=object_model.status,
            import_error=enrich_data.import_errors.get(offer_id),
            archive_date=enrich_data.get_archive_date(offer_id),
            on_premoderation=enrich_data.on_premoderation(offer_id)
        )
    elif status_tab.is_declined:
        result.declined_info = get_declined_info(
            status=object_model.status,
            offer_offence=enrich_data.get_offer_offence(offer_id=offer_id)
        )

    return result
