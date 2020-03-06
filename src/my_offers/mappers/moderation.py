from cian_entities import EntityMapper
from cian_entities.mappers import ValueMapper

from my_offers.entities.moderation import OfferOffence


offer_offence_mapper = EntityMapper(
    OfferOffence,
    without_camelcase=True,
    mappers={
        'created_date': ValueMapper(),
        'created_at': ValueMapper(),
        'updated_at': ValueMapper(),
    }
)
