from cian_entities import EntityMapper
from cian_entities.mappers import ValueMapper

from my_offers import entities


agent_mapper = EntityMapper(
    entities.Agent,
    without_camelcase=True,
    mappers={
        'created_at': ValueMapper(),
        'updated_at': ValueMapper(),
    }
)

agent_name_mapper = EntityMapper(
    entities.AgentName,
    without_camelcase=True,
)
