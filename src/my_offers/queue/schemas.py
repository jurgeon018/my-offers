from cian_schemas import EntitySchema

from my_offers.queue import entities


class RabbitMQAnnouncementMessageSchema(EntitySchema):
    class Meta:
        entity = entities.AnnouncementMessage
