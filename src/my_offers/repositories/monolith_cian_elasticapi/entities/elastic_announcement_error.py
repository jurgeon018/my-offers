# pylint: skip-file
"""

Code generated by cian-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client monolith-cian-elasticapi`

cian-codegen version: 1.4.1

"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class ElasticAnnouncementError:
    code: Optional[str] = None
    message: Optional[str] = None
    realty_object_id: Optional[int] = None