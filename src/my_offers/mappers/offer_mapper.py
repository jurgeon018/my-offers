from cian_entities import EntityMapper
from cian_entities.mappers import ValueMapper

from my_offers import entities


offer_mapper = EntityMapper(
    entities.Offer,
    without_camelcase=True,
    mappers={
        'sort_date': ValueMapper(),
        'raw_data': ValueMapper(),
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

offers_creation_date_mapper = EntityMapper(
    entities.OfferCreationDate,
    without_camelcase=True,
)

offer_row_version_mapper = EntityMapper(
    entities.OfferRowVersion,
    without_camelcase=True,
)

offer_similar_mapper = EntityMapper(
    entities.OfferSimilar,
    without_camelcase=True,
    mappers={
        'sort_date': ValueMapper(),
    }
)

offer_similar_with_type_mapper = EntityMapper(
    entities.OfferSimilarWithType,
    without_camelcase=True,
    mappers={
        'sort_date': ValueMapper(),
    }
)
