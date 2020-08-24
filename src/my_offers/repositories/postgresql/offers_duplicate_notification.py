from typing import Optional

import asyncpgsa
import sqlalchemy as sa
from sqlalchemy import and_, delete, select
from sqlalchemy.dialects.postgresql import insert

from my_offers import pg
from my_offers.entities.offer_duplicate_notification import OfferDuplicateNotification
from my_offers.repositories.postgresql.tables import metadata


offers_duplicate_notification = sa.Table(
    'offers_duplicate_notification',
    metadata,
    sa.Column('offer_id', sa.BIGINT, nullable=False),
    sa.Column('duplicate_offer_id', sa.BIGINT, nullable=False),
    sa.Column('send_at', sa.TIMESTAMP, nullable=False),
    sa.UniqueConstraint('offer_id', 'duplicate_offer_id'),
    # TODO: add notification type
)

offers_duplicate_email_notification = sa.Table(
    'offers_duplicate_email_notification',
    metadata,
    sa.Column('user_id', sa.BIGINT, nullable=False),
    sa.Column('subscription_id', sa.TEXT, nullable=False),
    sa.Column('email', sa.TEXT, nullable=False),
)

offers_email_notification_settings = sa.Table(
    'offers_email_notification_settings',
    metadata,
    sa.Column('user_id', sa.BIGINT, nullable=False),
    sa.Column('is_enabled', sa.BOOLEAN, nullable=False),
)


async def save_offers_duplicate_notification(notification: OfferDuplicateNotification) -> None:
    query, params = asyncpgsa.compile_query(
        insert(offers_duplicate_notification).values({
            'offer_id': notification.offer_id,
            'duplicate_offer_id': notification.duplicate_offer_id,
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
            offers_duplicate_email_notification.c.email
        ]).where(
            offers_duplicate_email_notification.c.user_id == user_id
        ))

    row = await pg.get().fetchrow(query, *params)

    return row['email'] if row else None


async def is_available_email_notification(user_id: int) -> bool:
    query, params = asyncpgsa.compile_query(
        select([
            offers_email_notification_settings.c.is_enabled
        ]).where(
            offers_email_notification_settings.c.user_id == user_id
        ))

    row = await pg.get().fetchrow(query, *params)

    return row['is_enabled'] if row else False
