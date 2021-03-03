import pytest

from my_offers.entities.mobile_offer import OfferDeactivatedService
from my_offers.enums.deactivated_service import DeactivatedServicesContext
from my_offers.repositories.monolith_cian_bill.entities import DeactivatedService
from my_offers.repositories.monolith_cian_bill.entities.deactivated_service import ServiceType
from my_offers.services.deactivated_service.get_deactivated_services import (
    _get_description,
    _get_offer_deactivated_services,
)


@pytest.mark.parametrize(
    ('context', 'service_names', 'is_auto_restore_on_payment_enabled', 'excepted'),
    (
        (
            DeactivatedServicesContext.undefined,
            [],
            True,
            None
        ), (
            DeactivatedServicesContext.highlight,
            ['выделение цветом'],
            True,
            'Выделение цветом отключено из-за нехватки средств. После пополнения баланса опция будет активирована '
            'автоматически.'
        ), (
            DeactivatedServicesContext.auction,
            ['ставка 23 ₽/сут.'],
            True,
            'Ставка 23 ₽/сут. отключена из-за нехватки средств. После пополнения баланса опция будет активирована'
            ' автоматически.'
        ), (
            DeactivatedServicesContext.highlight_and_auction,
            ['выделение цветом', 'ставка 23 ₽/сут.'],
            True,
            'Выделение цветом и ставка 23 ₽/сут. отключены из-за нехватки средств. После пополнения баланса'
            ' опции будут активированы автоматически.'
        ), (
            DeactivatedServicesContext.undefined,
            [],
            False,
            None
        ), (
            DeactivatedServicesContext.highlight,
            ['выделение цветом'],
            False,
            'Выделение цветом отключено из-за нехватки средств. Чтобы при пополнении баланса опция была'
            ' активирована, нажмите «Возобновить».'
        ), (
            DeactivatedServicesContext.auction,
            ['ставка 23 ₽/сут.'],
            False,
            'Ставка 23 ₽/сут. отключена из-за нехватки средств. Чтобы при пополнении баланса опция была'
            ' активирована, нажмите «Возобновить».'
        ), (
            DeactivatedServicesContext.highlight_and_auction,
            ['выделение цветом', 'ставка 23 ₽/сут.'],
            False,
            'Выделение цветом и ставка 23 ₽/сут. отключены из-за нехватки средств. Чтобы при пополнении баланса'
            ' опции были активированы, нажмите «Возобновить».'
        ),
    )
)
def test_get_description(context, service_names, is_auto_restore_on_payment_enabled, excepted):
    # act
    result = _get_description(context, service_names, is_auto_restore_on_payment_enabled)

    # assert
    assert result == excepted


@pytest.mark.parametrize(
    ('services', 'is_auto_restore_on_payment_enabled', 'excepted'),
    (
        (
            [DeactivatedService(announcement_id=123, service_type=ServiceType.auction, auction_bet=5)],
            True,
            OfferDeactivatedService(
                description='Ставка 5 ₽/сут. отключена из-за нехватки средств. После пополнения баланса опция '
                            'будет активирована автоматически.',
                is_auto_restore_on_payment_enabled=True
            )
        ), (
            [DeactivatedService(announcement_id=123, service_type=ServiceType.highlight, auction_bet=None)],
            False,
            OfferDeactivatedService(
                description='Выделение цветом отключено из-за нехватки средств. Чтобы при пополнении баланса опция была'
                            ' активирована, нажмите «Возобновить».',
                is_auto_restore_on_payment_enabled=False
            )
        ), (
            [
                DeactivatedService(announcement_id=123, service_type=ServiceType.highlight, auction_bet=None),
                DeactivatedService(announcement_id=123, service_type=ServiceType.auction, auction_bet=1),
            ],
            True,
            OfferDeactivatedService(
                description='Выделение цветом и ставка 1 ₽/сут. отключены из-за нехватки средств. После пополнения'
                            ' баланса опции будут активированы автоматически.',
                is_auto_restore_on_payment_enabled=True
            )
        ), (
            [
                DeactivatedService(announcement_id=123, service_type=ServiceType.highlight, auction_bet=None),
                DeactivatedService(announcement_id=123, service_type=ServiceType.auction, auction_bet=1),
                DeactivatedService(announcement_id=123, service_type=ServiceType.top3, auction_bet=None)
            ],
            True,
            OfferDeactivatedService(
                description=None,
                is_auto_restore_on_payment_enabled=True
            )
        ), (
            [DeactivatedService(announcement_id=123, service_type=ServiceType.calltracking, auction_bet=None)],
            True,
            OfferDeactivatedService(
                description=None,
                is_auto_restore_on_payment_enabled=True
            )
        ), (
            [DeactivatedService(announcement_id=123, service_type=ServiceType.debit_object, auction_bet=None)],
            False,
            OfferDeactivatedService(
                description=None,
                is_auto_restore_on_payment_enabled=False
            )
        ),
    ),
)
def test_get_offer_deactivated_services(services, is_auto_restore_on_payment_enabled, excepted):
    # act
    result = _get_offer_deactivated_services(services, is_auto_restore_on_payment_enabled)

    # assert
    assert result == excepted
