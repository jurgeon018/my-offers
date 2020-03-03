import pytest
from cian_test_utils import future

from my_offers.repositories.monolith_cian_ms_announcements.entities import CanUpdateEditdateResult, V1CanUpdateEditdate
from my_offers.services.announcement_api._can_update_edit_date import can_update_edit_date


@pytest.mark.gen_test
async def test_can_update_edit_date(mocker):
    # arrange
    v1_can_update_editdate_mock = mocker.patch(
        'my_offers.services.announcement_api._can_update_edit_date.v1_can_update_editdate',
        return_value=future([
            CanUpdateEditdateResult(can_update_edit_date=True, id=11),
            CanUpdateEditdateResult(can_update_edit_date=False, id=12),
            CanUpdateEditdateResult(can_update_edit_date=True, id=44),
        ])
    )

    expected = {11: True, 12: False, 14: False}

    # act
    result = await can_update_edit_date([11, 12, 14])

    # assert
    assert result == expected
    v1_can_update_editdate_mock.assert_called_once_with(V1CanUpdateEditdate(ids=[11, 12, 14]))
