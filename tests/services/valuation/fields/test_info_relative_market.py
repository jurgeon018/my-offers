import pytest

from my_offers.entities.valuation import InfoRelativeMarket
from my_offers.enums import PriceEstimate
from my_offers.services.valuation.fields.info_relative_market import get_info_relative_market


@pytest.mark.parametrize(
    ('market_price', 'real_price', 'expected'),
    (
        (1_000_000, 2_000_000, InfoRelativeMarket(
            price_estimate=PriceEstimate.more_market,
            title='Ваша цена выше рыночной',
            text='У объявлений с ценой выше рынка в среднем на 35% меньше просмотров.',
            hint='Согласно статистике просмотров объявлений похожих квартир за последние 12 дней.'
        )),
        (1_000_000, 500_000, InfoRelativeMarket(
            price_estimate=PriceEstimate.less_market,
            title='Ваша цена ниже рыночной',
            text='Квартиры с ценой ниже рынка и продвижением в среднем продаются в течение 30 дней.',
            hint='Согласно данным Циан.Аналитики за предыдущий год.'
        )),
        (1_000_000, 1_000_000, InfoRelativeMarket(
            price_estimate=PriceEstimate.in_market,
            title='Ваша цена рыночная',
            text='Квартиры с рыночной ценой и продвижением в среднем продаются в течение 45 дней.',
            hint='Согласно данным Циан.Аналитики за предыдущий год.'
        )),

    )
)
def test_get_info_relative_market(mocker, market_price, real_price, expected):
    # arrange & act
    result = get_info_relative_market(market_price=market_price, real_price=real_price)

    # assert
    assert result == expected
