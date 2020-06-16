from my_offers.entities.valuation import InfoRelativeMarket
from my_offers.enums import DealType, PriceEstimate


LOW_LIMIT = 0.9
HIGH_LIMIT = 1.1

LESS_MARKET = {
    'title': {
        DealType.rent: 'Ваша ставка ниже рыночной',
        DealType.sale: 'Ваша цена ниже рыночной',
    },
    'text': {
        DealType.rent: 'Квартиры с арендной ставкой ниже рынка и продвижением в среднем сдаются '
                       'менее\xa014\xa0дней.\xa0',
        DealType.sale: 'Квартиры с ценой ниже рынка и продвижением в среднем продаются в\xa0течение\xa030\xa0дней.\xa0',
    },
}

IN_MARKET = {
    'title': {
        DealType.rent: 'Ваша ставка рыночная',
        DealType.sale: 'Ваша цена рыночная',
    },
    'text': {
        DealType.rent: 'Квартиры с рыночной арендной ставкой и продвижением в среднем сдаются '
                       'в\xa0течение\xa014\xa0дней.\xa0',
        DealType.sale: 'Квартиры с рыночной ценой и продвижением в среднем продаются в\xa0течение\xa045\xa0дней.\xa0',
    },
}

MORE_MARKET = {
    'title': {
        DealType.rent: 'Ваша ставка выше рыночной',
        DealType.sale: 'Ваша цена выше рыночной',
    },
    'text': {
        DealType.rent: 'У объявлений с арендной ставкой выше рынка в среднем на\xa045%\xa0меньше\xa0просмотров.\xa0',
        DealType.sale: 'У объявлений с ценой выше рынка в среднем на\xa035%\xa0меньше\xa0просмотров.\xa0',
    },
}


def get_info_relative_market(
        *,
        deal_type: DealType,
        market_price: int,
        real_price: int,
) -> InfoRelativeMarket:
    if real_price < market_price * LOW_LIMIT:
        return InfoRelativeMarket(
            price_estimate=PriceEstimate.less_market,
            title=LESS_MARKET['title'][deal_type],
            text=LESS_MARKET['text'][deal_type],
            hint='Согласно данным Циан.Аналитики за предыдущий год.'
        )
    if market_price * LOW_LIMIT <= real_price <= market_price * HIGH_LIMIT:
        return InfoRelativeMarket(
            price_estimate=PriceEstimate.in_market,
            title=IN_MARKET['title'][deal_type],
            text=IN_MARKET['text'][deal_type],
            hint='Согласно данным Циан.Аналитики за предыдущий год.'
        )
    return InfoRelativeMarket(
        price_estimate=PriceEstimate.more_market,
        title=MORE_MARKET['title'][deal_type],
        text=MORE_MARKET['text'][deal_type],
        hint='Согласно статистике просмотров объявлений похожих квартир за последние 12 дней.'
    )
