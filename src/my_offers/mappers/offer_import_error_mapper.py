from cian_entities import EntityMapper
from cian_entities.mappers import ValueMapper

from my_offers import entities

offer_import_error_mapper = EntityMapper(
    entities.OfferImportError,
    without_camelcase=True,
    mappers={
        'created_at': ValueMapper(),
    }
)
