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
            text='У объявлений с арендной ставкой выше рынка в среднем на\xa045%\xa0меньше\xa0просмотров.\xa0',
            hint='Согласно статистике просмотров объявлений похожих квартир за последние 12 дней.'
        )),
        (DealType.rent, 1_000_000, 500_000, InfoRelativeMarket(
            price_estimate=PriceEstimate.less_market,
            title='Ваша ставка ниже рыночной',
            text='Квартиры с арендной ставкой ниже рынка и продвижением в среднем сдаются менее\xa014\xa0дней.\xa0',
            hint='Согласно данным Циан.Аналитики за предыдущий год.'
        )),
        (DealType.rent, 1_000_000, 1_000_003, InfoRelativeMarket(
            price_estimate=PriceEstimate.in_market,
            title='Ваша ставка рыночная',
            text='Квартиры с рыночной арендной ставкой и продвижением в среднем сдаются'
                 ' в\xa0течение\xa014\xa0дней.\xa0',
            hint='Согласно данным Циан.Аналитики за предыдущий год.'
        )),
        (DealType.sale, 1_000_000, 2_000_000, InfoRelativeMarket(
            price_estimate=PriceEstimate.more_market,
            title='Ваша цена выше рыночной',
            text='У объявлений с ценой выше рынка в среднем на\xa035%\xa0меньше\xa0просмотров.\xa0',
            hint='Согласно статистике просмотров объявлений похожих квартир за последние 12 дней.'
        )),
        (DealType.sale, 1_000_000, 500_000, InfoRelativeMarket(
            price_estimate=PriceEstimate.less_market,
            title='Ваша цена ниже рыночной',
            text='Квартиры с ценой ниже рынка и продвижением в среднем продаются в\xa0течение\xa030\xa0дней.\xa0',
            hint='Согласно данным Циан.Аналитики за предыдущий год.'
        )),
        (DealType.sale, 1_000_000, 1_000_003, InfoRelativeMarket(
            price_estimate=PriceEstimate.in_market,
            title='Ваша цена рыночная',
            text='Квартиры с рыночной ценой и продвижением в среднем продаются в\xa0течение\xa045\xa0дней.\xa0',
            hint='Согласно данным Циан.Аналитики за предыдущий год.'
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
