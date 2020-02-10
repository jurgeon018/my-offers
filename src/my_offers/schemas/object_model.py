from cian_schemas import EntitySchema

from my_offers.repositories.monolith_cian_announcementapi import entities as announcementapi_entities


class ObjectModelSchema(EntitySchema):
    class Meta:
        entity = announcementapi_entities.ObjectModel
