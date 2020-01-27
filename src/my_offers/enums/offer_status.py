from cian_enum import Enum, Value


class OfferStatus(Enum):
    """Статус объекта"""
    # todo: переделать на StrEnums
    new = Value(1, help='Новый')
    draft = Value(2, help='Черновик')
    check = Value(3, help='Проверяется')
    published = Value(4, help='Опубликован')
    deleted = Value(5, help='Удален')
    withdrawn = Value(6, help='Отозван')
    expired = Value(7, help='Истек')
