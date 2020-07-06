import asyncio
import logging
from dataclasses import dataclass, field
from typing import List

from cian_http.exceptions import ApiClientException, BadRequestException, TimeoutException
from cian_web.exceptions import BrokenRulesException, Error

from my_offers import entities, helpers
from my_offers.enums.actions import OfferActionStatus
from my_offers.repositories import monolith_cian_announcementapi
from my_offers.repositories.monolith_cian_announcementapi.entities import (
    AnnouncementProgressDto,
    AnnouncementsActionsV1GetJobStatus,
    ObjectModel,
)
from my_offers.repositories.monolith_cian_announcementapi.entities.get_job_status_response import State as JobState
from my_offers.services import agencies_settings
from my_offers.services.offers import load_object_model


logger = logging.getLogger(__name__)

END_STATUSES = [
    JobState.completed,
    JobState.error,
]


@dataclass
class MassActions:
    actor_id: int
    """ Пользователь-инициатор запуска операции """
    offers_ids: List[int] = field(default_factory=list)
    """Объявляния на которыми надо провести операцию """

    async def get_job_result(self, job_id: int, actor_id: int, delay: float) -> List[AnnouncementProgressDto]:
        """ Получение результата операции над объявлениями. """
        # TODO: https://jira.cian.tech/browse/CD-81998
        while True:
            await asyncio.sleep(delay)
            job_status = await monolith_cian_announcementapi.announcements_actions_v1_get_job_status(
                AnnouncementsActionsV1GetJobStatus(
                    job_id=job_id,
                    user_id=actor_id
                )
            )
            if job_status.state in END_STATUSES:
                break

        return job_status.announcements_progress or []

    async def _run_job(self) -> int:
        """ Запустить джобу и вернуть ID операции. """
        raise NotImplementedError

    async def execute(self, delay: float) -> List[AnnouncementProgressDto]:
        """ Запустить джобу и дождаться результата работы джобы.

            delay - частота запроса статуса выполнения операции.
        """
        job_id: int = await self._run_job()
        result = await self.get_job_result(
            job_id=job_id,
            actor_id=self.actor_id,
            delay=delay
        )
        return result


class OfferAction:

    def __init__(self, *, offer_id: int, user_id: int) -> None:
        self.offer_id = offer_id
        self.user_id = user_id

    async def execute(self) -> entities.OfferActionResponse:
        object_model = await load_object_model(user_id=self.user_id, offer_id=self.offer_id)
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

    def _get_action_code(self) -> str:
        raise NotImplementedError

    async def _check_rights(self, object_model: ObjectModel) -> None:
        agency_settings = await agencies_settings.get_settings_degradation_handler(self.user_id)
        available_actions = helpers.get_available_actions(
            status=object_model.status,
            is_archived=helpers.is_archived(object_model.flags),
            is_manual=helpers.is_manual(object_model.source),
            can_update_edit_date=True,
            agency_settings=agency_settings.value,
            is_in_hidden_base=object_model.is_in_hidden_base,
        )

        if not getattr(available_actions, self._get_action_code()):
            raise BrokenRulesException([
                Error(
                    message='Не хватает прав для выполнения данной операции',
                    code='not_enough_rights',
                    key='offer_id'
                )
            ])
