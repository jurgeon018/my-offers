from cian_core.context.handlers import RequestContextHandler
from cian_core.web import base_urls
from cian_web import get_handler
from tornado.web import url

from my_offers import entities
from my_offers.entities.get_offers import GetOfferV2
from my_offers.entities.qa import QaGetByIdRequest
from my_offers.services import actions, notifications, offers, qa, similars, valuation
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
        r'/public/v3/get-offers/$',
        get_handler(
            service=offers.v3_get_offers_public,
            method='POST',  # pragma: no mutate
            request_schema=entities.GetOffersRequest,
            response_schema=entities.GetOffersV3Response,
            base_handler_cls=PublicHandler,
        )
    ),
    url(
        r'/v3/get-offers/$',
        get_handler(
            service=offers.v3_get_offers_private,
            method='POST',  # pragma: no mutate
            request_schema=entities.GetOffersPrivateRequest,
            response_schema=entities.GetOffersV3Response,
            base_handler_cls=RequestContextHandler,
        )
    ),
    url(
        r'/public/v1/get-offers-counters/$',
        get_handler(
            service=offers.v1_get_offers_counters_public,
            response_schema=entities.OfferCounters,
            base_handler_cls=PublicHandler,
        )
    ),
    url(
        r'/v1/get-offers-ids-by-tab/$',
        get_handler(
            service=offers.get_offers_ids_by_tab,
            method='POST',  # pragma: no mutate
            request_schema=entities.GetOffersIdsByTabRequest,
            response_schema=entities.GetOffersIdsByTabResponse,
            base_handler_cls=RequestContextHandler,
        )
    ),
    url(
        r'/public/v1/get-offer-duplicates/$',
        get_handler(
            service=similars.v1_get_offer_similars_public,
            method='POST',  # pragma: no mutate
            request_schema=entities.GetOfferDuplicatesRequest,
            response_schema=entities.GetOfferDuplicatesResponse,
            base_handler_cls=PublicHandler,
        )
    ),
    url(
        r'/public/v1/get-offer-duplicates-tabs/$',
        get_handler(
            service=similars.v1_get_offer_similars_tabs_public,
            method='POST',  # pragma: no mutate
            request_schema=entities.GetOfferDuplicatesTabsRequest,
            response_schema=entities.GetOfferDuplicatesTabsResponse,
            base_handler_cls=PublicHandler,
        )
    ),
    url(
        r'/public/v1/get-offers-duplicates-for-desktop/$',
        get_handler(
            service=similars.v1_get_offer_similars_desktop_public,
            method='POST',  # pragma: no mutate
            request_schema=entities.GetOfferDuplicatesDesktopRequest,
            response_schema=entities.GetOfferDuplicatesDesktopResponse,
            base_handler_cls=PublicHandler,
        )
    ),
    url(
        r'/v1/get-offers-duplicates-count/$',
        get_handler(
            service=similars.v1_get_offers_similars_count,
            method='POST',  # pragma: no mutate
            request_schema=entities.GetOffersDuplicatesCountRequest,
            response_schema=entities.GetOffersDuplicatesCountResponse,
            base_handler_cls=RequestContextHandler,
        )
    ),
    url(
        r'/public/v1/get-offer-valuation/$',
        get_handler(
            service=valuation.v1_get_offer_valuation_public,
            method='POST',  # pragma: no mutate
            request_schema=entities.GetOfferValuationRequest,
            response_schema=entities.GetOfferValuationResponse,
            base_handler_cls=PublicHandler,
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
    url(
        r'/public/v1/subscribe-on-duplicates/$',
        get_handler(
            service=notifications.subscribe_on_duplicates,
            method='POST',  # pragma: no mutate
            request_schema=entities.SubscribeOnDuplicatesRequest,
            base_handler_cls=PublicHandler,
        )
    ),
    url(
        r'/public/v1/unsubscribe-on-duplicates/$',
        get_handler(
            service=notifications.unsubscribe_on_duplicates,
            method='POST',  # pragma: no mutate
            request_schema=entities.UnsubscribeOnDuplicatesRequest,
            base_handler_cls=PublicHandler,
        )
    ),
    url(
        r'/public/v1/get-notifications-settings/$',
        get_handler(
            service=notifications.get_notification_settings_public,
            method='GET',  # pragma: no mutate
            response_schema=entities.DuplicateSubscription,
            base_handler_cls=PublicHandler,
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
    url(
        r'/public/v1/actions/restore-offers/$',
        get_handler(
            service=actions.mass_offers_restore,
            method='POST',  # pragma: no mutate
            request_schema=entities.OffersMassRestoreRequest,
            response_schema=entities.OffersMassRestoreResponse,
            base_handler_cls=PublicHandler,
        )
    ),
    url(
        r'/public/v1/actions/change-offers-publisher/$',
        get_handler(
            service=actions.change_offers_publisher,
            method='POST',  # pragma: no mutate
            request_schema=entities.OffersChangePublisherRequest,
            response_schema=entities.OffersChangePublisherResponse,
            base_handler_cls=PublicHandler,
        )
    ),

    # calltracking
    url(
        r'/v1/get-offers-for-calltracking/$',
        get_handler(
            service=offers.get_offers_for_calltracking,
            method='POST',  # pragma: no mutate
            request_schema=entities.OffersForCalltrackingRequest,
            response_schema=entities.OffersForCalltrackingResponse,
            base_handler_cls=RequestContextHandler,
        )
    ),
    url(
        r'/v1/get-offers-for-calltracking-card/$',
        get_handler(
            service=offers.get_offers_for_calltracking_card,
            method='POST',  # pragma: no mutate
            request_schema=entities.OffersForCalltrackingRequest,
            response_schema=entities.OffersForCalltrackingCardResponse,
            base_handler_cls=RequestContextHandler,
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
