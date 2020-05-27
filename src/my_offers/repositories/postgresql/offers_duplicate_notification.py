import asyncpgsa
import sqlalchemy as sa
from sqlalchemy import delete
from sqlalchemy.dialects.postgresql import insert

from my_offers import pg
from my_offers.entities.offer_duplicate_notification import OfferDuplicateNotification


offers_duplicate_notification = sa.Table(
    sa.Column('offer_id', sa.BIGINT, nullable=False),
    sa.Column('duplicate_offer_id', sa.BIGINT, nullable=False),
    sa.Column('send_at', sa.TIMESTAMP, nullable=False),
    sa.UniqueConstraint('offer_id', 'duplicate_offer_id'),
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
        delete(offers_duplicate_notification).values({
            'offer_id': notification.offer_id,
            'duplicate_offer_id': notification.duplicate_offer_id,
        })
    )

    await pg.get().execute(query, *params)
