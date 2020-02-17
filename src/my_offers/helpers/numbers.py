def get_pretty_number(*, number: int, template: str = '%.0f') -> str:
    """ Получить число в "красивом" представлении.

        100 -> '100'
        1000 -> '1 000'
        10000 -> '10 000'
        100000 -> '100 000'
        1000000 -> '1 000 000'
    """
    number_str = str(template % number)

    if '.' in number_str:
        integral, fractional = number_str.split('.', 1)
    else:
        integral, fractional = number_str, ''

    result = []
    for _ in range(len(integral) // 3 + 1):
        result.append(integral[-3:])
        integral = integral[:-3]

    integral = ' '.join(reversed(list(filter(None, result))))
    if fractional.strip('0'):
        return f'{integral},{fractional}'

    return integral
