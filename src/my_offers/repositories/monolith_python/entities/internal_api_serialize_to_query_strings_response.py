# pylint: skip-file
"""

Code generated by cian-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client monolith-python`

cian-codegen version: 1.15.0

"""
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class InternalApiSerializeToQueryStringsResponse:
    query_strings: Optional[List[str]] = None
    """Список QueryString поисковых запросов"""
