from asyncpg import UniqueViolationError
from cian_web.exceptions import BrokenRulesException, Error
from simple_settings import settings

from my_offers.entities import NewEmailSubscription, SubscribeOnDuplicatesRequest, UnsubscribeOnDuplicatesRequest
from my_offers.helpers.emails import is_correct_email
from my_offers.repositories import postgresql


async def subscribe_on_duplicates(
        request: SubscribeOnDuplicatesRequest,
        realty_user_id: int
) -> None:
    """ Подписать пользователя на обновления дубликатов по всем активным объвлениям. """

    _validate_email(email=request.email)

    try:
        await postgresql.create_new_offers_subscription(subscription=NewEmailSubscription(
            user_id=realty_user_id,
            email=request.email
        ))
    except UniqueViolationError:
        raise BrokenRulesException(errors=[Error(
            key='email',
            code='user_already_subscribed',
            message=settings.EMAIL_USER_ALREADY_SUBSCRIBED_MSG
        )]) from None


async def unsubscribe_on_duplicates(
        request: UnsubscribeOnDuplicatesRequest,
        realty_user_id: int
) -> None:
    """ Отписаться от обновлений дубликаов по всем активным объявлениям. """

    _validate_email(email=request.email)

    is_subscribed = await postgresql.is_any_subscriptions_exists(user_id=realty_user_id)

    if not is_subscribed:
        raise BrokenRulesException(errors=[Error(
            key='email',
            code='user_is_not_subscribed',
            message=settings.EMAIL_USER_NOT_SUBSCRIBED_MSG
        )])

    await postgresql.delete_new_offers_subscription(user_id=realty_user_id, email=request.email)


def _validate_email(email: str) -> None:
    if not is_correct_email(email):
        raise BrokenRulesException(errors=[Error(
            key='email',
            code='incorrect_email',
            message=settings.EMAIL_VALIDATION_ERROR_MSG
        )])
