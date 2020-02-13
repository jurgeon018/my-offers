from cian_entities import EntityMapper

from my_offers.entities import GetOffersRequest


get_offers_request_mapper = EntityMapper(GetOffersRequest, without_camelcase=True,)
