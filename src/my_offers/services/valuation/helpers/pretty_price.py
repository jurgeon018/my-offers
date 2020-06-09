from my_offers.helpers.numbers import get_pretty_number


MILLION = 1_000_000


def get_pretty_market_price(price: int, need_million_str: bool = True) -> str:
    """ Получить цену в "красивом" представлении.
        100 -> '100'
        10000 -> '10 000'
        100000 -> '100 000'
        1000000 -> '1 млн'      need_million_str = True
        1700000 -> '1,7 млн'    need_million_str = True
        1000000 -> '1'          need_million_str = False
        1700000 -> '1,7'        need_million_str = False
    """
    if price < MILLION:
        return get_pretty_number(price)
    if price % MILLION == 0:
        price_str = str(price // MILLION)
    else:
        price_str = str(price / MILLION).replace('.', ',')
    return f'{price_str}{" млн" if need_million_str else ""}'


def get_pretty_price_diapason(price_min: int, price_max: int) -> str:
    """ Получить диапазон цен в "красивом" представлении.
        '1,7—2,1 млн'
        '0,8—1,1 млн'
        '50 000—60 000'
        '100 000—120 000'
    """
    if price_min >= MILLION or price_max >= MILLION:
        price_min_str = str(price_min / MILLION).replace('.', ',')
        price_max_str = get_pretty_market_price(price_max, need_million_str=False)
        return f'{price_min_str}—{price_max_str}\xa0млн'

    price_min_str = get_pretty_number(price_min)
    price_max_str = get_pretty_number(price_max)
    return f'{price_min_str}—{price_max_str}'
