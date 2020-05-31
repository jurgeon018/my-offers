from datetime import datetime

from my_offers import pg
from my_offers.entities.offer_duplicate_notification import OfferDuplicateNotification
from my_offers.repositories.postgresql.offers_duplicate_notification import (
    delete_offers_duplicate_notification,
    save_offers_duplicate_notification,
)


async def test_save_offers_duplicate_notification():
    # arrange
    notification = OfferDuplicateNotification(
        offer_id=1,
        duplicate_offer_id=2,
        send_at=datetime(2020, 5, 28)
    )

    # act
    await save_offers_duplicate_notification(notification)

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
        send_at=datetime(2020, 5, 28)
    )

    # act
    await delete_offers_duplicate_notification(notification)

    # assert
    pg.get().execute.assert_called_once_with(
        'DELETE FROM offers_duplicate_notification '
        'WHERE offers_duplicate_notification.offer_id = $2 AND offers_duplicate_notification.duplicate_offer_id = $1',
        2,
        1,
    )
