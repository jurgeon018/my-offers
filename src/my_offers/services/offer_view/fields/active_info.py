from my_offers.entities import get_offers
from my_offers.repositories.monolith_cian_announcementapi.entities import ObjectModel
from my_offers.services.offer_view.fields.from_package import is_from_package
from my_offers.services.offer_view.fields.is_autoprolong import is_autoprolong
from my_offers.services.offer_view.fields.publication_time_ends import is_publication_time_ends
from my_offers.services.offer_view.fields.publish_features import get_publish_features
from my_offers.services.offer_view.fields.vas import get_vas


def get_active_info(object_model: ObjectModel) -> get_offers.ActiveInfo:
    publish_terms = object_model.publish_terms
    terms = publish_terms.terms if publish_terms else None

    return get_offers.ActiveInfo(
        publish_features=get_publish_features(publish_terms),
        vas=get_vas(terms),
        is_from_package=is_from_package(terms),
        is_publication_time_ends=is_publication_time_ends(object_model),
        is_autoprolong=is_autoprolong(),
    )
