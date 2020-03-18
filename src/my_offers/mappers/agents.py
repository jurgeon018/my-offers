from cian_entities import EntityMapper
from cian_entities.mappers import ValueMapper

from my_offers.entities.agents import Agent


agent_mapper = EntityMapper(
    Agent,
    without_camelcase=True,
    mappers={
        'created_at': ValueMapper(),
        'updated_at': ValueMapper(),
    }
)
