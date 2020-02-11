from cian_automation.enums import Environment

from my_offers.settings.develop import *
from .base import *  # pylint: disable=wildcard-import,unused-wildcard-import

REPLACE_TEMPLATE_FOR_SERVICES = {
    'python-monolith': {Environment.dev: 'http://www.{ctx}.dev3.cian.ru'},
    'announcementapi': {Environment.dev: 'http://{ctx}.announcementapi.dev3.cian.ru'},
}
