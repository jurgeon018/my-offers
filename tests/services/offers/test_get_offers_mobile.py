import pytest
from cian_test_utils import future

from my_offers.repositories.moderation_checks_orchestrator.entities import UserIdentificationResult
from my_offers.repositories.moderation_checks_orchestrator.entities.user_identification_result import (
    IdentificationStatus,
)
from my_offers.services.mobile_offers.get_my_offers._get_unidentified_offers import _get_unidentified_offers


@pytest.mark.gen_test
async def test_get_unidentified_offers(mocker):
    # arrange
    mocker.patch(
        'cian_http.api_client.ApiAsyncClient.__call__',
        return_value=future([
            UserIdentificationResult(
                identification_status=IdentificationStatus.ok_no_identification_needed,
                user_id=12345,
                object_ids=None,
            )
        ])
    )
    expected = []

    # act
    result = await _get_unidentified_offers(user_id=123)

    # assert
    assert result == expected


@pytest.mark.gen_test
async def test_get_unidentified_empty_offers(mocker):
    # arrange
    mocker.patch(
        'cian_http.api_client.ApiAsyncClient.__call__',
        return_value=future([
            UserIdentificationResult(
                identification_status=IdentificationStatus.ok_no_identification_needed,
                user_id=123,
                object_ids=[1, 2, 3],
            )
        ])
    )
    expected = [1, 2, 3]

    # act
    result = await _get_unidentified_offers(user_id=123)

    # assert
    assert result == expected
