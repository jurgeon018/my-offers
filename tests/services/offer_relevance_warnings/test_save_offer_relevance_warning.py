from datetime import datetime
import pytest

import freezegun
import pytz
from freezegun.api import FakeDatetime
from cian_test_utils import future, v

from my_offers.entities.offer_relevance_warning import OfferRelevanceWarning
from my_offers.queue.entities import OfferRelevanceWarningMessage
from my_offers.queue.enums import OfferRelevanceCheckStatusId, OfferRelevanceTypeMessage
from my_offers.services.offer_relevance_warnings import save_offer_relevance_warning


@pytest.mark.parametrize('message, expected', (
    (
        OfferRelevanceWarningMessage(
            realty_object_id=111,
            guid='E19E639E-B488-4ADF-A367-55D84350B752',
            decline_date=None,
            check_status_id=OfferRelevanceCheckStatusId.relevance_confirmation_required.value,
            relevance_type_message=OfferRelevanceTypeMessage.warning_only.value,
        ),
        OfferRelevanceWarning(
            offer_id=111,
            check_id='E19E639E-B488-4ADF-A367-55D84350B752',
            due_date=None,
            finished=False,
            created_at=FakeDatetime(2020, 5, 20, tzinfo=pytz.UTC),
            updated_at=FakeDatetime(2020, 5, 20, tzinfo=pytz.UTC),
        ),
    ),
    (
        OfferRelevanceWarningMessage(
            realty_object_id=222,
            guid='CF576B6A-4A04-423D-A232-C21C73A9FE87',
            decline_date=datetime(2020, 4, 20),
            check_status_id=OfferRelevanceCheckStatusId.relevance_confirmation_required.value,
            relevance_type_message='other',
        ),
        OfferRelevanceWarning(
            offer_id=222,
            check_id='CF576B6A-4A04-423D-A232-C21C73A9FE87',
            due_date=datetime(2020, 4, 20),
            finished=False,
            created_at=FakeDatetime(2020, 5, 20, tzinfo=pytz.UTC),
            updated_at=FakeDatetime(2020, 5, 20, tzinfo=pytz.UTC),
        ),
    ),
    (
        OfferRelevanceWarningMessage(
            realty_object_id=222,
            guid='CF576B6A-4A04-423D-A232-C21C73A9FE87',
            decline_date=None,
            check_status_id='other',
            relevance_type_message='other',
        ),
        OfferRelevanceWarning(
            offer_id=222,
            check_id='CF576B6A-4A04-423D-A232-C21C73A9FE87',
            due_date=None,
            finished=True,
            created_at=FakeDatetime(2020, 5, 20, tzinfo=pytz.UTC),
            updated_at=FakeDatetime(2020, 5, 20, tzinfo=pytz.UTC),
        ),
    )
))
@pytest.mark.gen_test
@freezegun.freeze_time('2020-05-20')
async def test_save_offer_relevance_warning(mocker, message, expected):
    # arrange
    psql_save_offer_relevance_warning_mock = mocker.patch(
        'my_offers.services.offer_relevance_warnings._save_offer_relevance_warning'
        '.postgresql.save_offer_relevance_warning',
        return_value=future(),
    )

    # act
    await save_offer_relevance_warning(v(message))

    # assert
    psql_save_offer_relevance_warning_mock.assert_called_once_with(v(expected))
