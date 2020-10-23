from my_offers.enums.notifications import DuplicateNotificationType
from my_offers.repositories.notification_center import v1_mobile_push_get_settings
from my_offers.repositories.notification_center.entities import (
    GetMobilePushSettingsRequest,
    GetMobilePushSettingsResponse,
)
from my_offers.repositories.notification_center.entities.get_mobile_push_settings_request import OsType


async def is_mobile_push_enabled(*, user_id: int, push_type: DuplicateNotificationType) -> bool:
    response: GetMobilePushSettingsResponse = await v1_mobile_push_get_settings(
        GetMobilePushSettingsRequest(
            user_id=str(user_id),
            is_authenticated=True,
            os_type=OsType.android,
        ))

    for item in response.items:
        for child_item in item.children:
            if child_item.id == push_type.value:
                return child_item.is_active

    return False
