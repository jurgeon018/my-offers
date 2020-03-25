import os

from simple_settings import settings


def _get_branch_suffix() -> str:
    branch_suffix = os.getenv('BRANCH_NAME', '')
    if branch_suffix and 'master' not in branch_suffix:
        return '.' + branch_suffix
    return ''


def get_modified_queue_name(queue_name: str) -> str:
    return f'{settings.APPLICATION_NAME}.{queue_name}{_get_branch_suffix()}'
