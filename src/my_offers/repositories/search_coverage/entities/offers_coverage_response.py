# pylint: skip-file
"""

Code generated by cian-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client search-coverage`

cian-codegen version: 1.4.2

"""
from dataclasses import dataclass
from typing import List

from .offer_coverage import OfferCoverage


@dataclass
class OffersCoverageResponse:
    data: List[OfferCoverage]
    """Статистика по объявлениям"""
