from cian_automation.enums import Environment

from .base import *  # pylint: disable=wildcard-import,unused-wildcard-import


REPLACE_TEMPLATE_FOR_SERVICES = {
    'python-monolith': {Environment.stage: 'https://www.{ctx}.stage.cian.ru'},
    'announcementapi': {Environment.stage: 'http://{ctx}.announcement.api.stage.cian.ru'},
}
