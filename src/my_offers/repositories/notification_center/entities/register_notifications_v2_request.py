# pylint: skip-file
"""

Code generated by cian-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client notification-center`

cian-codegen version: 1.4.3

"""
from dataclasses import dataclass
from typing import List

from .register_notification_v2_request import RegisterNotificationV2Request


@dataclass
class RegisterNotificationsV2Request:
    notifications: List[RegisterNotificationV2Request]
    """Список уведомлений"""
