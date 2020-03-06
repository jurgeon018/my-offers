from my_offers.entities import get_offers
from my_offers.repositories.monolith_cian_announcementapi.entities import ObjectModel
from my_offers.services.offer_view.fields import (
    get_moderation,
    get_not_active_info,
    get_publish_features,
    get_vas,
    is_autoprolong,
    is_from_package,
    is_publication_time_ends,
)
from my_offers.services.offers.enrich.enrich_data import EnrichData


def get_page_specific_info(
        *,
        object_model: ObjectModel,
        enrich_data: EnrichData
) -> get_offers.PageSpecificInfo:
    publish_terms = object_model.publish_terms
    terms = publish_terms.terms if publish_terms else None

    return get_offers.PageSpecificInfo(
        active_info=get_offers.ActiveInfo(
            publish_features=get_publish_features(publish_terms),
            vas=get_vas(terms),
            is_from_package=is_from_package(terms),
            is_publication_time_ends=is_publication_time_ends(object_model),
            is_autoprolong=is_autoprolong(),
        ),
        not_active_info=get_not_active_info(
            status=object_model.status,
            import_error=enrich_data.import_errors.get(object_model.id)
        ),
        declined_info=get_offers.DeclinedInfo(
            moderation=get_moderation(
                status=object_model.status,
                offer_offence=enrich_data.get_offer_offence(offer_id=object_model.id)
            )
        ),
    )
