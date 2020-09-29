from cian_automation.enums import Environment

from .base import *  # pylint: disable=wildcard-import,unused-wildcard-import


REPLACE_TEMPLATE_FOR_SERVICES = {
    'python-monolith': {Environment.prod: 'https://www.cian.ru'},
    'announcementapi': {Environment.prod: 'http://announcementapi.cian.ru'},
}
X_PASS_KEY = '8758C73D-D54B-408D-A714-F3B6F684644B'
HEADERS.update({'X-PassKey': X_PASS_KEY})
