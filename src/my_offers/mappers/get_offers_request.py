from cian_entities import EntityMapper

from my_offers.entities.get_offers import Filter


get_offers_filters_mapper = EntityMapper(Filter, without_camelcase=True)
