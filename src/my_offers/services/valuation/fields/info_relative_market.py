from my_offers.entities.valuation import InfoRelativeMarket
from my_offers.enums import PriceEstimate


LOW_LIMIT = 0.9
HIGH_LIMIT = 1.1


def get_info_relative_market(
        market_price: int,
        real_price: int,
) -> InfoRelativeMarket:
    if real_price < market_price * LOW_LIMIT:
        return InfoRelativeMarket(
            price_estimate=PriceEstimate.less_market,
            title='Ваша цена ниже рыночной',
            text='Квартиры с ценой ниже рынка и продвижением в среднем продаются в течение 30 дней.',
            hint='Согласно данным Циан.Аналитики за предыдущий год.'
        )
    if market_price * LOW_LIMIT <= real_price <= market_price * HIGH_LIMIT:
        return InfoRelativeMarket(
            price_estimate=PriceEstimate.in_market,
            title='Ваша цена рыночная',
            text='Квартиры с рыночной ценой и продвижением в среднем продаются в течение 45 дней.',
            hint='Согласно данным Циан.Аналитики за предыдущий год.'
        )
    return InfoRelativeMarket(
        price_estimate=PriceEstimate.more_market,
        title='Ваша цена выше рыночной',
        text='У объявлеений с ценой выше рынка в среднем на 35% меньше просмотров.',
        hint='Согласно статистике просмотров объявлений похожих квартир за последние 12 дней.'
    )
