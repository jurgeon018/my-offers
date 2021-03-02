from itertools import groupby
from operator import attrgetter
from typing import List, Dict, Optional

from cian_core.degradation import get_degradation_handler
from my_offers.entities.mobile_offer import OfferDeactivatedService
from my_offers.enums.deactivated_service import DeactivatedServicesContext
from my_offers.repositories.monolith_cian_bill import v1_tariffication_get_deactivated_additional_services
from my_offers.repositories.monolith_cian_bill.entities import V1TarifficationGetDeactivatedAdditionalServices, \
    GetDeactivatedAdditionalServicesResponse, DeactivatedService


def _get_description(
    context: DeactivatedServicesContext,
    service_names: List[str],
    is_auto_restore_on_payment_enabled: bool
) -> Optional[str]:
    if context == DeactivatedServicesContext.highlight:
        deactivated = 'отключено'
    elif context == DeactivatedServicesContext.auction:
        deactivated = 'отключена'
    elif context == DeactivatedServicesContext.highlight_and_auction:
        deactivated = 'отключены'
    else:
        return None

    if context == DeactivatedServicesContext.highlight_and_auction:
        options_will = u'опции будут активированы'
        options_were = u'опции были активированы'
    else:
        options_will = u'опция будет активирована'
        options_were = u'опция была активирована'

    if is_auto_restore_on_payment_enabled:
        what = f'После пополнения баланса {options_will} автоматически.'
    else:
        what = f'Чтобы при пополнении баланса {options_were}, нажмите «Возобновить».'

    return f'{" и ".join(service_names).capitalize()} {deactivated} из-за нехватки средств. {what}'


def _get_offer_deactivated_services(
    services: List[DeactivatedService],
    is_auto_restore_on_payment_enabled: bool
):
    contexts = []
    service_names = []
    for service in services:
        if service.service_type.is_highlight:
            contexts.append(DeactivatedServicesContext.highlight)
            service_names.append('выделение цветом')
        elif service.service_type.is_auction:
            contexts.append(DeactivatedServicesContext.auction)
            service_names.append(f'ставка {service.auction_bet} ₽/сут.')

    if len(services) > 2:
        context = DeactivatedServicesContext.undefined
    elif len(contexts) == 2:
        context = DeactivatedServicesContext.highlight_and_auction
    else:
        context = contexts[0]

    return OfferDeactivatedService(
        is_auto_restore_on_payment_enabled=is_auto_restore_on_payment_enabled,
        description=_get_description(
            context=context,
            service_names=service_names,
            is_auto_restore_on_payment_enabled=is_auto_restore_on_payment_enabled,
        )
    )


def get_deactivated_services_for_offers(
    user_id: int,
    offer_ids: List[int]
) -> Dict[int, OfferDeactivatedService]:

    response: GetDeactivatedAdditionalServicesResponse
    response = await v1_tariffication_get_deactivated_additional_services(
        V1TarifficationGetDeactivatedAdditionalServices(
            user_id=user_id,
            announcement_ids=offer_ids
        )
    )

    keyfunc = attrgetter('announcement_id')
    sorted_services = sorted(response.deactivated_services, key=keyfunc)

    result: Dict[int, OfferDeactivatedService] = {
        offer_id: _get_offer_deactivated_services(
            services=list(services),
            is_auto_restore_on_payment_enabled=response.is_auto_restore_on_payment_enabled,
        )
        for offer_id, services in groupby(sorted_services, key=keyfunc)
    }

    return result


get_deactivated_services_degradation_handler = get_degradation_handler(
    func=get_deactivated_services_for_offers,
    key='monolith_cian_bill.get_deactivated_services',
    default={},
)
