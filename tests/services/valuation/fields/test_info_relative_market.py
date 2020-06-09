import pytest

from my_offers.entities.valuation import InfoRelativeMarket
from my_offers.enums import DealType, PriceEstimate
from my_offers.services.valuation.fields.info_relative_market import get_info_relative_market


@pytest.mark.parametrize(
    ('deal_type', 'market_price', 'real_price', 'expected'),
    (
        (DealType.rent, 1_000_000, 2_000_000, InfoRelativeMarket(
            price_estimate=PriceEstimate.more_market,
            title='Ваша ставка выше рыночной',
            text='У объявлений с арендной ставкой выше рынка в среднем на 45% меньше просмотров',
            hint='Согласно статистике просмотров объявлений похожих квартир за последние 12 месяцев'
        )),
        (DealType.rent, 1_000_000, 500_000, InfoRelativeMarket(
            price_estimate=PriceEstimate.less_market,
            title='Ваша ставка ниже рыночной',
            text='Квартиры с арендной ставкой ниже рынка и продвижением в среднем сдаются менее 14 дней',
            hint='По данным Циан.Аналитика за предыдущий год'
        )),
        (DealType.rent, 1_000_000, 1_000_003, InfoRelativeMarket(
            price_estimate=PriceEstimate.in_market,
            title='Ваша ставка рыночная',
            text='Квартиры с рыночной арендной ставкой и продвижением в среднем сдаются в течение 14 дней',
            hint='По данным Циан.Аналитика за предыдущий год'
        )),
        (DealType.sale, 1_000_000, 2_000_000, InfoRelativeMarket(
            price_estimate=PriceEstimate.more_market,
            title='Ваша цена выше рыночной',
            text='У объявлений с ценой выше рынка в среднем на 35% меньше просмотров',
            hint='Согласно статистике просмотров объявлений похожих квартир за последние 12 месяцев'
        )),
        (DealType.sale, 1_000_000, 500_000, InfoRelativeMarket(
            price_estimate=PriceEstimate.less_market,
            title='Ваша цена ниже рыночной',
            text='Квартиры с ценой ниже рынка и продвижением в среднем продаются в течение 30 дней',
            hint='По данным Циан.Аналитика за предыдущий год'
        )),
        (DealType.sale, 1_000_000, 1_000_003, InfoRelativeMarket(
            price_estimate=PriceEstimate.in_market,
            title='Ваша цена рыночная',
            text='Квартиры с рыночной ценой и продвижением в среднем продаются в течение 45 дней',
            hint='По данным Циан.Аналитика за предыдущий год'
        )),

    )
)
def test_get_info_relative_market(mocker, deal_type, market_price, real_price, expected):
    # arrange & act
    result = get_info_relative_market(
        deal_type=deal_type,
        market_price=market_price,
        real_price=real_price,
    )

    # assert
    assert result == expected
