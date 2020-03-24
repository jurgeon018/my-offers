from typing import Optional

from cian_core.degradation import get_degradation_handler

from my_offers.repositories.agencies_settings import v1_get_settings
from my_offers.repositories.agencies_settings.entities import AgencySettings, V1GetSettings


async def get_settings(user_id: int) -> Optional[AgencySettings]:
    return await v1_get_settings(V1GetSettings(user_id))

get_settings_degradation_handler = get_degradation_handler(
    func=get_settings,
    key='get_settings',
    default=None,
)
