from cian_entities import EntityMapper
from cian_entities.mappers import ValueMapper

from my_offers import entities


offer_mapper = EntityMapper(
    entities.Offer,
    without_camelcase=True,
    mappers={
        'sort_date': ValueMapper(),
    }
)
