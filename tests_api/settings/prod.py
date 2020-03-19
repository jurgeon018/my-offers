from cian_automation.enums import Environment
from .base import *  # pylint: disable=wildcard-import,unused-wildcard-import


REPLACE_TEMPLATE_FOR_SERVICES = {
    'python-monolith': {Environment.prod: 'https://www.cian.ru'},
    'announcementapi': {Environment.prod: 'http://announcementapi.cian.ru'},
}
