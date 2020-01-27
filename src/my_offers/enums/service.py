from cian_enum import Enum, Value


class Service(Enum):
    # todo: переделать на StrEnums
    free = Value(1, help=u'Бесплатная публикация')
    paid = Value(2, help=u'Платная публикация')
    premium = Value(3, help=u'Премиум-публикация')
    top3 = Value(4, help=u'Tоп-публикация')
    highlight = Value(5, help=u'Выделение цветом')
    calltracking = Value(6, help=u'Колтрекинг')
    auction = Value(7, help=u'Аукцион')
    demand = Value(8, help=u'Спрос')
    demand_package = Value(9, help=u'Пакет заявок')