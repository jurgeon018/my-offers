from typing import Any, Dict, Optional

from cian_core.web.base_handlers import PublicHandler as BasePublicHandler


class PublicHandler(BasePublicHandler):
    # pylint: disable=abstract-method

    @property
    def realty_user_id(self) -> Optional[int]:
        value = self.request.headers.get('X-Real-UserId')
        return int(value) if value and value.isdigit() else None

    def get_extra_kwargs(self) -> Dict[str, Any]:
        return {
            'realty_user_id': self.realty_user_id,
        }
