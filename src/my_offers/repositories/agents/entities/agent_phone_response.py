# pylint: skip-file
"""

Code generated by cian-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client agents`

cian-codegen version: 1.15.1

"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class AgentPhoneResponse:
    """Телефон сотрудника"""

    is_confirmed: bool
    """Признак подтвержденности номера"""
    is_main: bool
    """Признак основного номера"""
    phone: Optional[str] = None
    """Номер телефона"""