# pylint: skip-file
"""

Code generated by cian-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client monolith-cian-announcementapi`

cian-codegen version: 1.4.1

"""
from dataclasses import dataclass


@dataclass
class RestoreResponse:
    job_id: int
    """Id задачи."""
