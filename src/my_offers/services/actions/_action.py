import logging

from cian_http.exceptions import ApiClientException, BadRequestException, TimeoutException
from cian_web.exceptions import BrokenRulesException, Error

from my_offers import entities
from my_offers.enums.offer_action_status import OfferActionStatus
from my_offers.repositories.monolith_cian_announcementapi.entities import ObjectModel
from my_offers.repositories.postgresql.object_model import get_object_model


logger = logging.getLogger(__name__)


class OfferAction:
    def __init__(self, *, offer_id: int, user_id: int) -> None:
        self.offer_id = offer_id
        self.user_id = user_id

    async def execute(self) -> entities.OfferActionResponse:
        object_model = await self._load_object_model()
        await self._check_rights(object_model)

        try:
            await self._run_action(object_model)
        except BadRequestException as e:
            logger.exception('Offer action BrokenRulesException offer_id %s', self.offer_id)
            raise BrokenRulesException([
                Error(
                    message=e.message.strip(),
                    code='operation_error',
                    key='offer_id'
                )
            ])
        except TimeoutException:
            logger.exception('Offer action TimeoutException offer_id %s', self.offer_id)
            raise BrokenRulesException([
                Error(
                    message='Ошибка при выполнении операции',
                    code='operation_timeout',
                    key='offer_id'
                )
            ])
        except ApiClientException:
            logger.exception('Offer action ApiClientException offer_id %s', self.offer_id)
            raise BrokenRulesException([
                Error(
                    message='Ошибка при выполнении операции',
                    code='operation_unknown_error',
                    key='offer_id'
                )
            ])

        return entities.OfferActionResponse(status=OfferActionStatus.ok)

    async def _run_action(self, object_model: ObjectModel) -> None:
        raise NotImplementedError

    async def _load_object_model(self) -> ObjectModel:
        object_model = await get_object_model({'offer_id': self.offer_id})
        # todo: https://jira.cian.tech/browse/CD-74186 проверить доступ
        if not object_model:
            raise BrokenRulesException([
                Error(
                    message='Объявление не найдено',
                    code='not_found',
                    key='offer_id'
                )
            ])

        return object_model

    async def _check_rights(self, object_model: ObjectModel) -> None:
        # todo: https://jira.cian.tech/browse/CD-74186
        if self.user_id != object_model.user_id:
            raise BrokenRulesException([
                Error(
                    message='Не хватает прав для выполнения данной операции',
                    code='not_enough_rights',
                    key='offer_id'
                )
            ])
