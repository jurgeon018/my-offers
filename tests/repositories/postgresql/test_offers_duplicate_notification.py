from datetime import datetime

from cian_test_utils import future

from my_offers import pg
from my_offers.entities.offer_duplicate_notification import OfferDuplicateNotification
from my_offers.enums.notifications import UserNotificationType
from my_offers.repositories import postgresql


async def test_save_offers_duplicate_notification():
    # arrange
    notification = OfferDuplicateNotification(
        offer_id=1,
        duplicate_offer_id=2,
        send_at=datetime(2020, 5, 28),
        notification_type=UserNotificationType.mobile_push
    )

    # act
    await postgresql.save_offers_duplicate_notification(notification)

    # assert
    pg.get().execute.assert_called_once_with(
        'INSERT INTO offers_duplicate_notification (offer_id, duplicate_offer_id, send_at) VALUES ($2, $1, $3)',
        2,
        1,
        datetime(2020, 5, 28)
    )


async def test_delete_offers_duplicate_notification():
    # arrange
    notification = OfferDuplicateNotification(
        offer_id=1,
        duplicate_offer_id=2,
        send_at=datetime(2020, 5, 28),
        notification_type=UserNotificationType.mobile_push
    )

    # act
    await postgresql.delete_offers_duplicate_notification(notification)

    # assert
    pg.get().execute.assert_called_once_with(
        'DELETE FROM offers_duplicate_notification '
        'WHERE offers_duplicate_notification.offer_id = $2 AND offers_duplicate_notification.duplicate_offer_id = $1',
        2,
        1,
    )


async def test_get_user_email():
    # arrange
    user_id = 111
    pg.get().fetchrow.return_value = future({'email': 'kek@lol.com'})

    # act
    await postgresql.get_user_email(user_id=user_id)

    # assert
    pg.get().fetchrow.assert_called_once_with(
        'SELECT offers_duplicate_email_notification.email '
        '\nFROM offers_duplicate_email_notification '
        '\nWHERE offers_duplicate_email_notification.user_id = $1',
        user_id
    )


async def test_is_available_email_notification():
    # arrange
    user_id = 111
    pg.get().fetchrow.return_value = future({'is_enabled': True})

    # act
    await postgresql.is_available_email_notification(user_id=user_id)

    # assert
    pg.get().fetchrow.assert_called_once_with(
        'SELECT offers_email_notification_settings.is_enabled '
        '\nFROM offers_email_notification_settings '
        '\nWHERE offers_email_notification_settings.user_id = $1',
        user_id
    )
