import math
from typing import Union


def get_pretty_number(number: Union[int, float]) -> str:
    """ Получить число в "красивом" представлении.

        100 -> '100'
        1000 -> '1 000'
        10000 -> '10 000'
        100000 -> '100 000'
        1000000 -> '1 000 000'
    """
    number = math.ceil(number)

    number_str = str('%.0f' % number)

    result = []
    for _ in range(len(number_str) // 3 + 1):
        result.append(number_str[-3:])
        number_str = number_str[:-3]

    return ' '.join(reversed(list(filter(None, result))))
