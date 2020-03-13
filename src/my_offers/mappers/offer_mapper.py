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

reindex_offer_item_mapper = EntityMapper(
    entities.ReindexOfferItem,
    without_camelcase=True,
    mappers={
        'created_at': ValueMapper(),
    }
)

reindex_offer_mapper = EntityMapper(
    entities.ReindexOffer,
    without_camelcase=True,
    mappers={
        'updated_at': ValueMapper(),
    }
)
