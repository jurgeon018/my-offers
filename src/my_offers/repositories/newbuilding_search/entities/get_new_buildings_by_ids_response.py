# pylint: skip-file
"""

Code generated by cian-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client newbuilding-search`

cian-codegen version: 1.4.1

"""
from dataclasses import dataclass
from typing import List

from .get_newbuilding_by_ids_item import GetNewbuildingByIdsItem


@dataclass
class GetNewBuildingsByIdsResponse:
    items: List[GetNewbuildingByIdsItem]
    """Объект ЖК"""
