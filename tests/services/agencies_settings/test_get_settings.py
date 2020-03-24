import pytest
from cian_test_utils import future

from my_offers.repositories.agencies_settings.entities import AgencySettings, V1GetSettings
from my_offers.services.agencies_settings._get_settings import get_settings


@pytest.mark.gen_test
async def test_get_settings(mocker):
    # arrange
    v1_get_settings_mock = mocker.patch(
        'my_offers.services.agencies_settings._get_settings.v1_get_settings',
        return_value=future(
            AgencySettings(
                can_sub_agents_edit_offers_from_xml=False,
                can_sub_agents_publish_offers=False,
                can_sub_agents_view_agency_balance=False,
                display_all_agency_offers=False,
            )
        )
    )

    expected = AgencySettings(
        can_sub_agents_edit_offers_from_xml=False,
        can_sub_agents_publish_offers=False,
        can_sub_agents_view_agency_balance=False,
        display_all_agency_offers=False,
    )

    # act
    result = await get_settings(111)

    # assert
    assert result == expected
    v1_get_settings_mock.assert_called_once_with(V1GetSettings(agency_id=111))
