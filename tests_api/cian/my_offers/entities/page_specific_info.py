# pylint: skip-file
"""

Code generated by new-codegen; DO NOT EDIT.

To re-generate, run `new-codegen generate-client my-offers`

new-codegen version: 4.0.2

"""
from dataclasses import dataclass
from typing import Optional

from .active_info import ActiveInfo
from .declined_info import DeclinedInfo
from .not_active_info import NotActiveInfo


@dataclass
class PageSpecificInfo:
    activeInfo: Optional[ActiveInfo] = None
    """Доп. информация для вкладки активные"""
    declinedInfo: Optional[DeclinedInfo] = None
    """Доп. информация для вкладки отклоненные"""
    notActiveInfo: Optional[NotActiveInfo] = None
    """Доп. информация для вкладки неактивные"""