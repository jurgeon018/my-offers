from cian_entities import EntityMapper

from my_offers import entities


offer_mapper = EntityMapper(
    entities.Offer,
    without_camelcase=True,
)
