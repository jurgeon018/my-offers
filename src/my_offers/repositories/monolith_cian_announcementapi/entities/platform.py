# pylint: skip-file
"""

Code generated by cian-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client monolith-cian-announcementapi`

cian-codegen version: 1.4.1

"""
from dataclasses import dataclass
from typing import Optional

from cian_enum import NoFormat, StrEnum


class Type(StrEnum):
    __value_format__ = NoFormat
    web_site = 'webSite'
    android = 'android'
    ios = 'ios'
    upload = 'upload'
    app = 'app'
    qa_autotests = 'qaAutotests'


@dataclass
class Platform:
    type: Optional[Type] = None
    version: Optional[str] = None
