from typing import List, Optional

from my_offers import enums
from my_offers.helpers.numbers import get_pretty_number
from my_offers.repositories.monolith_cian_announcementapi.entities import BargainTerms
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Category, CoworkingOfferType
from my_offers.services.offer_view.constants import CURRENCY, SQUARE_METER_SYMBOL


def get_features(
        *,
        bargain_terms: BargainTerms,
        category: Category,
        total_area: Optional[float],
        offer_type: enums.OfferType,
        deal_type: enums.DealType,
        coworking_offer_type: Optional[CoworkingOfferType],
) -> List[str]:
    is_commercial = offer_type.is_commercial
    is_newobject = category.is_new_building_flat_sale

    currency = CURRENCY.get(bargain_terms.currency)
    is_square_meter = bargain_terms.price_type and bargain_terms.price_type.is_square_meter
    is_all = bargain_terms.price_type and bargain_terms.price_type.is_all
    sale_type = bargain_terms.sale_type
    lease_type = bargain_terms.lease_type
    price = bargain_terms.price

    features = []

    # TODO: https://jira.cian.tech/browse/CD-74195
    # TODO: восстановить тесты https://jira.cian.tech/browse/CD-77783
    if deal_type.is_sale:
        if bargain_terms.mortgage_allowed:
            features.append('Возможна ипотека')

        if sale_type and sale_type.is_free:
            features.append('Свободная продажа')

        if sale_type and sale_type.is_alternative:
            features.append('Альтернативная продажа')

        if (is_commercial or is_newobject) and is_square_meter and currency and price:
            pretty_price = get_pretty_number(price)
            features.append(f'{pretty_price} {currency} {SQUARE_METER_SYMBOL}')

        if not is_commercial and sale_type and sale_type.is_dupt:
            features.append('Переуступка')

        if is_all and currency and total_area and price:
            pretty_price = get_pretty_number(price / total_area)
            features.append(f'{pretty_price} {currency} за {SQUARE_METER_SYMBOL}')
    else:
        if bargain_terms.agent_fee:
            features.append(f'Агенту: {bargain_terms.agent_fee}%')

        if bargain_terms.client_fee:
            features.append(f'Клиенту: {bargain_terms.client_fee}%')

        if bargain_terms.deposit and currency:
            features.append(f'Залог: {bargain_terms.deposit} {currency}')

        if is_commercial:
            if coworking_offer_type and coworking_offer_type.is_office:
                pretty_price = get_pretty_number(price)
                features.append(f'{pretty_price}\xa0{currency}/мес. за весь офис')
            elif is_square_meter and currency and price:
                if bargain_terms.payment_period and bargain_terms.payment_period.is_monthly:
                    months_count = 12
                else:
                    months_count = 1
                pretty_price = get_pretty_number(price * months_count)
                features.append(f'{pretty_price} {currency} за {SQUARE_METER_SYMBOL} в год')

            if lease_type and lease_type.is_sublease:
                features.append('Субаренда')

            if lease_type and lease_type.is_direct:
                features.append('Прямая аренда')

    return features
