from datetime import datetime

import pytest
from cian_test_utils import future

from my_offers import pg
from my_offers.entities.moderation import OfferOffence
from my_offers.enums import ModerationOffenceStatus
from my_offers.mappers.moderation import offer_offence_mapper
from my_offers.repositories import postgresql


pytestmark = pytest.mark.gen_test


async def test_save_offer_offence(mocker):
    # arrange
    now = datetime(2020, 12, 12)
    offer_offence = OfferOffence(
        offence_id=555,
        offence_type=1,
        offence_text='ТЕСТ',
        offence_status=ModerationOffenceStatus.confirmed,
        offer_id=777,
        created_by=888,
        created_date=datetime(2020, 1, 1),
        row_version=0,
        updated_at=now,
        created_at=now,
    )

    # act
    await postgresql.save_offer_offence(offer_offence=offer_offence)

    # assert
    pg.get().execute.assert_called_once_with(
        'INSERT INTO offers_offences (offence_id, offence_type, offence_text, offence_status, offer_id, row_version, '
        'created_by, created_date, created_at, updated_at) '
        'VALUES ($4, $7, $6, $5, $8, $19, $2, $3, $1, $20) '
        'ON CONFLICT (offence_id) '
        'DO UPDATE SET offence_id = $9, offence_type = $10, offence_text = $11, offence_status = $12, offer_id = $13, '
        'row_version = $14, created_by = $15, created_date = $16, updated_at = $17 '
        'WHERE offers_offences.row_version < $18',
        offer_offence.updated_at,
        offer_offence.created_by,
        offer_offence.created_date,
        offer_offence.offence_id,
        offer_offence.offence_status.value,
        offer_offence.offence_text,
        offer_offence.offence_type,
        offer_offence.offer_id,
        offer_offence.offence_id,
        offer_offence.offence_type,
        offer_offence.offence_text,
        offer_offence.offence_status.value,
        offer_offence.offer_id,
        offer_offence.row_version,
        offer_offence.created_by,
        offer_offence.created_date,
        offer_offence.created_at,
        offer_offence.row_version,
        offer_offence.row_version,
        offer_offence.updated_at,
    )


async def test_get_offer_offence(mocker):
    # arrange
    offer_id = 1
    now = datetime(2020, 12, 12)
    offer_offence = dict(
        offence_id=555,
        offence_type=1,
        offence_text='ТЕСТ',
        offence_status=ModerationOffenceStatus.confirmed,
        offer_id=offer_id,
        created_by=888,
        created_date=datetime(2020, 1, 1),
        row_version=0,
        updated_at=now,
        created_at=now,
    )
    pg.get().fetchrow.return_value = future(offer_offence)

    # act
    result = await postgresql.get_offer_offence(offer_id=offer_id, status=ModerationOffenceStatus.confirmed)

    # assert
    assert result == offer_offence_mapper.map_from(offer_offence)
    pg.get().fetchrow.assert_called_once_with(
        'SELECT offers_offences.offence_id, offers_offences.offence_type, offers_offences.offence_text, '
        'offers_offences.offence_status, offers_offences.offer_id, offers_offences.row_version, '
        'offers_offences.created_by, offers_offences.created_date, offers_offences.created_at, '
        'offers_offences.updated_at '
        '\nFROM offers_offences '
        '\nWHERE offers_offences.offer_id = $2 '
        'AND offers_offences.offence_status = $1',
        ModerationOffenceStatus.confirmed.value,
        offer_id
    )


async def test_get_offer_offence__offence_is_none(mocker):
    # arrange
    offer_id = 1
    pg.get().fetchrow.return_value = future([])

    # act
    result = await postgresql.get_offer_offence(offer_id=offer_id, status=ModerationOffenceStatus.confirmed)

    # assert
    assert result is None
    pg.get().fetchrow.assert_called_once_with(
        'SELECT offers_offences.offence_id, offers_offences.offence_type, offers_offences.offence_text, '
        'offers_offences.offence_status, offers_offences.offer_id, offers_offences.row_version, '
        'offers_offences.created_by, offers_offences.created_date, offers_offences.created_at, '
        'offers_offences.updated_at '
        '\nFROM offers_offences '
        '\nWHERE offers_offences.offer_id = $2 '
        'AND offers_offences.offence_status = $1',
        ModerationOffenceStatus.confirmed.value,
        offer_id
    )
