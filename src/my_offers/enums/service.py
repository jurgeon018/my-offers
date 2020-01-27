from cian_enum import Enum, Value


class Service(Enum):
    # todo: переделать на StrEnums
    free = Value(1, help='Бесплатная публикация')
    paid = Value(2, help='Платная публикация')
    premium = Value(3, help='Премиум-публикация')
    top3 = Value(4, help='Tоп-публикация')
    highlight = Value(5, help='Выделение цветом')
    calltracking = Value(6, help='Колтрекинг')
    auction = Value(7, help='Аукцион')
    demand = Value(8, help='Спрос')
    demand_package = Value(9, help='Пакет заявок')
