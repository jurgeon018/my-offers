import pytest
from cian_test_utils import future

from my_offers.repositories.monolith_cian_ms_announcements.entities import UpdateEditdateRequest, UpdateEditdateResult
from my_offers.repositories.monolith_cian_ms_announcements.entities.update_editdate_result import Result
from my_offers.services.announcement_api import update_edit_date


@pytest.mark.gen_test
async def test_update_edit_date(mocker):
    # arrange
    v1_update_editdate_mock = mocker.patch(
        'my_offers.services.announcement_api._update_edit_date.v1_update_editdate',
        return_value=future([
            UpdateEditdateResult(id=11, result=Result.success),
            UpdateEditdateResult(id=12, result=Result.error),
            UpdateEditdateResult(id=44, result=Result.success),
            UpdateEditdateResult(id=None, result=None),
            UpdateEditdateResult(id=None, result=Result.success),
            UpdateEditdateResult(id=15, result=None),
        ])
    )
    expected = {11: True, 12: False, 14: False, 15: False}

    # act
    result = await update_edit_date([11, 12, 14, 15])

    # assert
    assert result == expected
    v1_update_editdate_mock.assert_called_once_with(UpdateEditdateRequest(ids=[11, 12, 14, 15]))
