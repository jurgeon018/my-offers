# pylint: skip-file
"""

Code generated by cian-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client monolith-cian-ms-announcements`

cian-codegen version: 1.4.1

"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class CanUpdateEditdateResult:
    """Возможность обновления даты публикации для объявления."""

    can_update_edit_date: Optional[bool] = None
    """Возможность обновления даты публикации."""
    id: Optional[int] = None
    """Id объявления."""