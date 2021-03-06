# pylint: skip-file
"""

Code generated by cian-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client monolith-python`

cian-codegen version: 1.15.0

"""
from dataclasses import dataclass

from cian_enum import NoFormat, StrEnum

from .internal_api_serialize_to_query_strings_response import InternalApiSerializeToQueryStringsResponse


class Status(StrEnum):
    __value_format__ = NoFormat
    ok = 'ok'


@dataclass
class SerializeToQueryStringsResponse:
    data: InternalApiSerializeToQueryStringsResponse
    status: Status
