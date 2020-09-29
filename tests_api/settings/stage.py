from cian_automation.enums import Environment

from .base import *  # pylint: disable=wildcard-import,unused-wildcard-import


REPLACE_TEMPLATE_FOR_SERVICES = {
    'python-monolith': {Environment.stage: 'https://www.{ctx}.stage.cian.ru'},
    'announcementapi': {Environment.stage: 'http://{ctx}.announcement.api.stage.cian.ru'},
}
X_PASS_KEY = '8758C73D-D54B-408D-A714-F3B6F684644B'
HEADERS.update({'X-PassKey': X_PASS_KEY})
