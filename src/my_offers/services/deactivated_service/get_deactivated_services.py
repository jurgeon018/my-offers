from typing import Dict, List, Optional

from my_offers.entities.mobile_offer import OfferDeactivatedService
from my_offers.enums.deactivated_service import DeactivatedServicesContext
from my_offers.repositories.monolith_cian_bill import v1_tariffication_get_deactivated_additional_services
from my_offers.repositories.monolith_cian_bill.entities import (
    DeactivatedService,
    GetDeactivatedAdditionalServicesResponse,
    V1TarifficationGetDeactivatedAdditionalServices,
)


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
        options_will = 'опции будут активированы'
        options_were = 'опции были активированы'
    else:
        options_will = 'опция будет активирована'
        options_were = 'опция была активирована'

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


async def get_deactivated_services_for_offers(
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

    offer_id_services: Dict[int, List[DeactivatedService]] = {}
    for service in response.deactivated_services:
        if offer_id_services.get(service.announcement_id):
            offer_id_services[service.announcement_id].append(service)
        else:
            offer_id_services[service.announcement_id] = [service]

    result: Dict[int, OfferDeactivatedService] = {}
    for offer_id, services in offer_id_services.items():
        result[offer_id] = _get_offer_deactivated_services(
            services=services,
            is_auto_restore_on_payment_enabled=response.is_auto_restore_on_payment_enabled,
        )

    return result
