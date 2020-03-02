from cian_entities import EntityMapper
from cian_entities.mappers import ValueMapper

from my_offers.entities.billing import OfferBillingContract


offer_billing_contract_mapper = EntityMapper(
    OfferBillingContract,
    without_camelcase=True,
    mappers={
        'start_date': ValueMapper(),
        'payed_till': ValueMapper(),
        'created_at': ValueMapper(),
        'updated_at': ValueMapper(),
    }
)
