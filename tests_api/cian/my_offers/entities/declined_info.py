# pylint: skip-file
"""

Code generated by new-codegen; DO NOT EDIT.

To re-generate, run `new-codegen generate-client my-offers`

new-codegen version: 4.0.2

"""
from dataclasses import dataclass
from typing import Optional

from .moderation import Moderation


@dataclass
class DeclinedInfo:
    moderation: Optional[Moderation] = None
    """Данные о причине отклонения объявления"""