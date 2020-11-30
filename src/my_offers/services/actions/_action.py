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
from my_offers.services.offers._get_offers import get_agent_hierarchy_data_degradation_handler


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

    async def _get_job_result(self, job_id: int, actor_id: int, delay: float) -> List[AnnouncementProgressDto]:
        """ Получение результата операции над объявлениями. """
        # TODO: https://jira.cian.tech/browse/CD-81998

        job_status = None
        while True:
            await asyncio.sleep(delay)

            try:
                job_status = await monolith_cian_announcementapi.announcements_actions_v1_get_job_status(
                    AnnouncementsActionsV1GetJobStatus(
                        job_id=job_id,
                        user_id=actor_id
                    )
                )
            except ApiClientException:
                logger.warning('Failed to get status job: %s', job_id, exc_info=True)
                continue

            if job_status.state in END_STATUSES:
                break

        return job_status.announcements_progress if job_status else []

    async def _run_job(self) -> int:
        """ Запустить джобу и вернуть ID операции. """
        raise NotImplementedError

    async def _run_job_with_handle_errors(self) -> int:
        """ Запустить джобу и вернуть ID операции. Прокидывает все 400 из вызываемой апи. """
        try:
            job_id: int = await self._run_job()
            return job_id
        except ApiClientException as exc:
            if exc.code == 400:
                raise BrokenRulesException(errors=[Error(
                    key=e.key,
                    code=e.code,
                    message=e.message
                ) for e in exc.errors])
            raise exc

    async def execute(self, delay: float) -> List[AnnouncementProgressDto]:
        """ Запустить джобу и дождаться результата работы джобы.

            delay - частота запроса статуса выполнения операции.
        """
        job_id = await self._run_job_with_handle_errors()
        result = await self._get_job_result(
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
        (
            agency_settings,
            agent_hierarchy_data,
        ) = await asyncio.gather(
            agencies_settings.get_settings_degradation_handler(self.user_id),
            get_agent_hierarchy_data_degradation_handler(self.user_id),
        )
        available_actions = helpers.get_available_actions(
            status=object_model.status,
            is_archived=helpers.is_archived(object_model.flags),
            is_manual=helpers.is_manual(object_model.source),
            can_update_edit_date=True,
            agency_settings=agency_settings.value,
            is_in_hidden_base=object_model.is_in_hidden_base,
            agent_hierarchy_data=agent_hierarchy_data.value,
        )

        if not getattr(available_actions, self._get_action_code()):
            raise BrokenRulesException([
                Error(
                    message='Не хватает прав для выполнения данной операции',
                    code='not_enough_rights',
                    key='offer_id'
                )
            ])
