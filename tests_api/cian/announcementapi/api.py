# pylint: skip-file
"""

Code generated by new-codegen; DO NOT EDIT.

To re-generate, run `new-codegen generate-client announcementapi`

new-codegen version: 4.0.2

"""
from cian_automation.context import LazyImport

from .clients.v2_announcements_add import V2AnnouncementsAdd


class Announcementapi(metaclass=LazyImport):
    v2_announcements_add: V2AnnouncementsAdd
