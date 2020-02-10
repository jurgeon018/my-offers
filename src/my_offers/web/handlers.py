from typing import Any, Dict, Optional

from cian_core.web.base_handlers import PublicHandler as BasePublicHandler
from cian_web import get_handler

from my_offers import entities
from my_offers.services import offers


class PublicHandler(BasePublicHandler):

    @property
    def realty_user_id(self) -> Optional[int]:
        value = self.request.headers.get('X-Real-UserId')
        return int(value) if value and value.isdigit() else None

    def get_extra_kwargs(self) -> Dict[str, Any]:
        return {
            'realty_user_id': self.realty_user_id,
        }


GetOffersHandler = get_handler(
    service=offers.get_offers,
    method='POST',  # pragma: no mutate
    request_schema=entities.GetOffersRequest,
    response_schema=entities.GetOffersResponse,
    base_handler_cls=PublicHandler,
)
