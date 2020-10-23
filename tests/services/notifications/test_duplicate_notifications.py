import pytest
from asyncpg import UniqueViolationError
from cian_json import json
from cian_test_utils import future
from simple_settings import settings

from my_offers.entities.offer_duplicate_notification import OfferDuplicateNotification
from my_offers.enums.notifications import UserNotificationType
from my_offers.helpers.category import get_types
from my_offers.helpers.title import get_offer_title
from my_offers.repositories.emails.entities import SendEmailByEmailRequest, SendEmailByEmailResponse
from my_offers.repositories.emails.entities.send_email_by_email_response import Status as EmailStatus
from my_offers.repositories.monolith_cian_announcementapi.entities import BargainTerms, ObjectModel, Phone
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Category
from my_offers.services.notifications import send_email_new_duplicate_notification, send_new_duplicates_notification
from my_offers.services.offer_view.fields import get_offer_url


pytestmark = pytest.mark.gen_test


async def test_send_email_duplicate_notification__check_sensitive_email_params(mocker):
    # arrange
    email = 'kek@example.com'
    offer = ObjectModel(
        id=111,
        cian_id=111,
        bargain_terms=BargainTerms(price=123),
        category=Category.flat_rent,
        phones=[Phone(country_code='1', number='12312')]

    )
    duplicate_offer = ObjectModel(
        id=222,
        cian_id=222,
        bargain_terms=BargainTerms(price=123),
        category=Category.flat_rent,
        phones=[Phone(country_code='1', number='12312')]

    )
    offer_type, deal_type = get_types(offer.category)
    parameters = {
        'ObjectName': get_offer_title(object_model=offer),
        'ObjectLink': get_offer_url(cian_offer_id=offer.cian_id, offer_type=offer_type, deal_type=deal_type),
        'DoubleObject': get_offer_title(object_model=duplicate_offer),
        'DoubleObjectLink': get_offer_url(
            cian_offer_id=duplicate_offer.cian_id,
            offer_type=offer_type,
            deal_type=deal_type
        ),
        'UnsubscribeLetter': settings.EMAIL_UNSUBSCRIBE_URL
    }

    emails_v2_send_email_mock = mocker.patch(
        'my_offers.services.notifications._new_duplicate_notifications.emails_v2_send_email',
        return_value=future(SendEmailByEmailResponse())
    )

    # act
    await send_email_new_duplicate_notification(
        email=email,
        offer=offer,
        duplicate_offer=duplicate_offer
    )

    # assert
    emails_v2_send_email_mock.assert_called_once_with(
        SendEmailByEmailRequest(
            address_list=[email],
            template_name=settings.EMAIL_DUPLICATE_TEMPLATE,
            parameters=json.dumps(parameters)
        ))


async def test_send_email_duplicate_notification__email_is_none(mocker):
    # arrange
    email = None
    offer = ...
    duplicate_offer = ...

    emails_v2_send_email_mock = mocker.patch(
        'my_offers.services.notifications._new_duplicate_notifications.emails_v2_send_email',
    )

    # act
    await send_email_new_duplicate_notification(
        email=email,
        offer=offer,
        duplicate_offer=duplicate_offer
    )

    # assert
    emails_v2_send_email_mock.assert_not_called()


async def test_send_email_duplicate_notification__user_not_found_in_emails_service(mocker):
    # arrange
    email = 'kek@example.com'
    offer = ObjectModel(
        id=111,
        cian_id=111,
        bargain_terms=BargainTerms(price=123),
        category=Category.flat_rent,
        phones=[Phone(country_code='1', number='12312')]

    )
    duplicate_offer = ObjectModel(
        id=222,
        cian_id=222,
        bargain_terms=BargainTerms(price=123),
        category=Category.flat_rent,
        phones=[Phone(country_code='1', number='12312')]

    )
    mocker.patch(
        'my_offers.services.notifications._new_duplicate_notifications.emails_v2_send_email',
        return_value=future(SendEmailByEmailResponse(status=EmailStatus.user_not_found))
    )
    logger_mock = mocker.patch(
        'my_offers.services.notifications._new_duplicate_notifications.logger',
    )

    # act
    await send_email_new_duplicate_notification(
        email=email,
        offer=offer,
        duplicate_offer=duplicate_offer
    )

    # assert
    logger_mock.error('User not found in `emails` service')


async def test_send_duplicates_notification__already_send_notification(mocker):
    # arrange
    offer = ObjectModel(
        id=111,
        bargain_terms=BargainTerms(price=123),
        category=Category.flat_rent,
        phones=[Phone(country_code='1', number='12312')]

    )
    duplicate_offer = ObjectModel(
        id=222,
        bargain_terms=BargainTerms(price=123),
        category=Category.flat_rent,
        phones=[Phone(country_code='1', number='12312')]

    )
    mocker.patch(
        'my_offers.services.notifications._new_duplicate_notifications.get_notification_types',
        return_value=future([UserNotificationType.mobile_push])
    )
    mocker.patch(
        'my_offers.services.notifications._new_duplicate_notifications.postgresql.save_offers_duplicate_notification',
        side_effect=UniqueViolationError
    )
    send_email_duplicate_notification_mock = mocker.patch(
        'my_offers.services.notifications._new_duplicate_notifications.send_email_new_duplicate_notification',
    )
    send_mobile_duplicate_notification_mock = mocker.patch(
        'my_offers.services.notifications._new_duplicate_notifications.send_mobile_new_duplicate_notification',
    )

    # act
    await send_new_duplicates_notification(
        user_id=123,
        offer=offer,
        duplicate_offer=duplicate_offer
    )

    # assert
    send_email_duplicate_notification_mock.assert_not_called()
    send_mobile_duplicate_notification_mock.assert_not_called()


async def test_send_duplicates_notification__error_while_send_notification(mocker):
    # arrange
    offer = ObjectModel(
        id=111,
        bargain_terms=BargainTerms(price=123),
        category=Category.flat_rent,
        phones=[Phone(country_code='1', number='12312')]

    )
    duplicate_offer = ObjectModel(
        id=222,
        bargain_terms=BargainTerms(price=123),
        category=Category.flat_rent,
        phones=[Phone(country_code='1', number='12312')]

    )
    mocker.patch(
        'my_offers.services.notifications._new_duplicate_notifications.get_notification_types',
        return_value=future([UserNotificationType.mobile_push])
    )
    mocker.patch(
        'my_offers.services.notifications._new_duplicate_notifications.postgresql.save_offers_duplicate_notification',
        return_value=future()
    )
    mocker.patch(
        'my_offers.services.notifications._new_duplicate_notifications.send_mobile_new_duplicate_notification',
        side_effect=Exception
    )
    delete_offers_duplicate_notification_mock = mocker.patch(
        'my_offers.services.notifications._new_duplicate_notifications.postgresql.delete_offers_duplicate_notification',
        return_value=future()
    )

    # act
    with pytest.raises(Exception):
        await send_new_duplicates_notification(
            user_id=123,
            offer=offer,
            duplicate_offer=duplicate_offer
        )

    # assert
    delete_offers_duplicate_notification_mock.assert_called_once_with(
        OfferDuplicateNotification(
            offer_id=offer.id,
            duplicate_offer_id=duplicate_offer.id,
            send_at=mocker.ANY,
            notification_type=UserNotificationType.mobile_push
        )
    )
