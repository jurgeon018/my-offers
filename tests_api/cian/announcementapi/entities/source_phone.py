# pylint: skip-file
"""

Code generated by new-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client announcementapi`

new-codegen version: 4.0.1

"""
from dataclasses import dataclass


@dataclass
class SourcePhone:
    countryCode: str
    """Код страны"""
    number: str
    """Номер"""
