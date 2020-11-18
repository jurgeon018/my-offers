from cian_entities import EntityMapper
from cian_entities.mappers import ValueMapper

from my_offers import entities


offer_relevance_warning_mapper = EntityMapper(
    entities.OfferRelevanceWarning,
    without_camelcase=True,
    mappers={
        'created_at': ValueMapper(),
        'due_date': ValueMapper(),
        'updated_at': ValueMapper(),
    }
)


offer_relevance_warning_info_mapper = EntityMapper(
    entities.OfferRelevanceWarningInfo,
    without_camelcase=True,
)
