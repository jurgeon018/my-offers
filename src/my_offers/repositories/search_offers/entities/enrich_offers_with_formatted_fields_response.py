# pylint: skip-file
"""

Code generated by cian-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client search-offers`

cian-codegen version: 1.9.0

"""
from dataclasses import dataclass
from typing import List, Optional

from .enrich_offers_with_formatted_fields_item import EnrichOffersWithFormattedFieldsItem


@dataclass
class EnrichOffersWithFormattedFieldsResponse:
    formatted_data: Optional[List[EnrichOffersWithFormattedFieldsItem]] = None
    """Словарь с id и форматированными полями"""
