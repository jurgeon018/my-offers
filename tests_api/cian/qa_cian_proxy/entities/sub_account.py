# pylint: skip-file
"""

Code generated by new-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client qa-cian-proxy`

new-codegen version: 4.0.0

"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class SubAccount:
    email: Optional[str] = None
    """Email."""
    password: Optional[str] = None
    """Пароль."""
    userId: Optional[int] = None
    """Id."""