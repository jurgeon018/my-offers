from cian_enum import Enum, Value


class RealtyRegions(Enum):
    moscow = Value(1, 'Москва')
    moscow_area = Value(4593, 'Московская область')
    moscow_and_area = Value(-1, 'Москва и область')
    st_petersburg = Value(2, 'Санкт-Петербург')
    st_petersburg_area = Value(4588, 'Ленинградская область')
    st_petersburg_and_area = Value(-2, 'Санкт-Петербург и область')
    krasnodar = Value(4820, 'Краснодар')
    krasnodar_area = Value(4584, 'Краснодарская область')
    anapa = Value(174191, 'Анапа')
