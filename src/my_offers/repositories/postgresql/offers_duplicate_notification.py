from typing import Optional

import asyncpgsa
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as psa
from sqlalchemy import and_, delete, select
from sqlalchemy.dialects.postgresql import insert

from my_offers import pg
from my_offers.entities import NewEmailSubscription
from my_offers.entities.offer_duplicate_notification import OfferDuplicateNotification
from my_offers.enums.notifications import UserNotificationType
from my_offers.helpers.tables import get_names
from my_offers.repositories.postgresql.tables import metadata


_notification_type = psa.ENUM(*get_names(UserNotificationType), name='notification_type', )
offers_duplicate_notification = sa.Table(
    'offers_duplicate_notification',
    metadata,
    sa.Column('offer_id', sa.BIGINT, nullable=False),
    sa.Column('duplicate_offer_id', sa.BIGINT, nullable=False),
    sa.Column('send_at', sa.TIMESTAMP, nullable=False),
    sa.Column('notification_type', sa.TEXT, nullable=True)
)

offers_email_notification_settings = sa.Table(
    'offers_email_notification_settings',
    metadata,
    sa.Column('user_id', sa.BIGINT, nullable=False),
    sa.Column('subscription_id', sa.TEXT, nullable=False),
    sa.Column('email', sa.TEXT, nullable=False),
)


async def save_offers_duplicate_notification(notification: OfferDuplicateNotification) -> None:
    notification_type = notification.notification_type.value if notification.notification_type else None
    query, params = asyncpgsa.compile_query(
        insert(offers_duplicate_notification).values({
            'offer_id': notification.offer_id,
            'duplicate_offer_id': notification.duplicate_offer_id,
            'notification_type': notification_type,
            'send_at': notification.send_at,
        })
    )

    await pg.get().execute(query, *params)


async def delete_offers_duplicate_notification(notification: OfferDuplicateNotification) -> None:
    query, params = asyncpgsa.compile_query(
        delete(offers_duplicate_notification).where(
            and_(
                offers_duplicate_notification.c.offer_id == notification.offer_id,
                offers_duplicate_notification.c.duplicate_offer_id == notification.duplicate_offer_id,
            )
        )
    )

    await pg.get().execute(query, *params)


async def get_user_email(user_id: int) -> Optional[str]:
    query, params = asyncpgsa.compile_query(
        select([
            offers_email_notification_settings.c.email
        ]).where(
            offers_email_notification_settings.c.user_id == user_id
        ))

    row = await pg.get().fetchrow(query, *params)

    return row['email'] if row else None


async def is_any_subscriptions_exists(user_id: int) -> bool:
    query = 'SELECT 1 as result FROM offers_email_notification_settings WHERE user_id = $1 LIMIT 1'
    params = [
        user_id,
    ]

    row = await pg.get().fetchrow(query, *params)

    return bool(row['result']) if row else False


async def create_new_offers_subscription(subscription: NewEmailSubscription) -> None:
    query, params = asyncpgsa.compile_query(
        insert(offers_email_notification_settings).values({
            'user_id': subscription.user_id,
            'email': subscription.email,
        })
    )

    await pg.get().execute(query, *params)


async def delete_new_offers_subscription(*, user_id: int) -> None:
    query = 'DELETE FROM offers_email_notification_settings WHERE user_id = $1'
    params = [
        user_id,
    ]

    await pg.get().execute(query, *params)
