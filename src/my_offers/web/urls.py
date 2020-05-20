from cian_core.context.handlers import RequestContextHandler
from cian_core.web import base_urls
from cian_web import get_handler
from tornado.web import url

from my_offers import entities
from my_offers.entities.get_offers import GetOfferV2
from my_offers.entities.qa import QaGetByIdRequest
from my_offers.services import actions, duplicates, offers, qa
from my_offers.web.handlers import PublicHandler


urlpatterns = base_urls.urlpatterns + [
    url(
        r'/public/v2/get-offers/$',
        get_handler(
            service=offers.v2_get_offers_public,
            method='POST',  # pragma: no mutate
            request_schema=entities.GetOffersRequest,
            response_schema=entities.GetOffersV2Response,
            base_handler_cls=PublicHandler,
        )
    ),
    url(
        r'/v2/get-offers/$',
        get_handler(
            service=offers.v2_get_offers_private,
            method='POST',  # pragma: no mutate
            request_schema=entities.GetOffersPrivateRequest,
            response_schema=entities.GetOffersV2Response,
            base_handler_cls=RequestContextHandler,
        )
    ),
    url(
        r'/public/v1/get-offer-duplicates/$',
        get_handler(
            service=duplicates.v1_get_offer_duplicates_public,
            method='POST',  # pragma: no mutate
            request_schema=entities.GetOfferDuplicatesRequest,
            response_schema=entities.GetOfferDuplicatesResponse,
            base_handler_cls=PublicHandler,
        )
    ),
    url(
        r'/v1/get-offers-duplicates-count/$',
        get_handler(
            service=duplicates.v1_get_offers_duplicates_count,
            method='POST',  # pragma: no mutate
            request_schema=entities.GetOffersDuplicatesCountRequest,
            response_schema=entities.GetOffersDuplicatesCountResponse,
            base_handler_cls=RequestContextHandler,
        )
    ),
    url(
        r'/v1/update-offer/',
        get_handler(
            service=offers.update_offer,
            method='POST',  # pragma: no mutate
            request_schema=entities.UpdateOfferRequest,
            base_handler_cls=RequestContextHandler,
        )
    ),

    # Actions
    url(
        r'/public/v1/actions/archive-offer/$',
        get_handler(
            service=actions.archive_offer,
            method='POST',  # pragma: no mutate
            request_schema=entities.OfferActionRequest,
            response_schema=entities.OfferActionResponse,
            base_handler_cls=PublicHandler,
        )
    ),
    url(
        r'/public/v1/actions/delete-offer/$',
        get_handler(
            service=actions.delete_offer,
            method='POST',  # pragma: no mutate
            request_schema=entities.OfferActionRequest,
            response_schema=entities.OfferActionResponse,
            base_handler_cls=PublicHandler,
        )
    ),
    url(
        r'/public/v1/actions/update-edit-date/$',
        get_handler(
            service=actions.update_edit_date,
            method='POST',  # pragma: no mutate
            request_schema=entities.OfferActionRequest,
            response_schema=entities.OfferActionResponse,
            base_handler_cls=PublicHandler,
        )
    ),

    # public API
    url(
        r'/v1/get-offers-creation-date/$',
        get_handler(
            service=offers.get_offers_creation_date,
            method='POST',  # pragma: no mutate
            request_schema=entities.OffersCreationDateRequest,
            response_schema=entities.OffersCreationDateResponse,
            base_handler_cls=RequestContextHandler,
        )
    ),

    # QA
    url(
        r'/qa/v1/get-offer/$',
        get_handler(
            service=qa.get_offer,
            method='GET',  # pragma: no mutate
            request_schema=QaGetByIdRequest,
            response_schema=entities.Offer,
            base_handler_cls=RequestContextHandler,
        )),
    url(
        r'/qa/v1/get-offer-view/',
        get_handler(
            service=qa.get_offer_view,
            method='GET',  # pragma: no mutate
            request_schema=QaGetByIdRequest,
            response_schema=GetOfferV2,
            base_handler_cls=RequestContextHandler,
        )
    ),
]
