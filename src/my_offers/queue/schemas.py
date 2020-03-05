from cian_schemas import EntitySchema

from my_offers import entities
from my_offers.queue import entities as mq_entities


class RabbitMQAnnouncementMessageSchema(EntitySchema):
    class Meta:
        entity = mq_entities.AnnouncementMessage


class RabbitMQOffenceMessageSchema(EntitySchema):
    class Meta:
        entity = entities.ModerationOfferOffence


class RabbitMQServiceContractCreatedMessageSchema(EntitySchema):
    class Meta:
        entity = entities.ServiceContractMessage


class RabbitMQSaveUnloadErrorMessageSchema(EntitySchema):
    class Meta:
        entity = entities.SaveUnloadErrorMessage
