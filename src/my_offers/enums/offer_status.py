from cian_enum import Enum, Value


class OfferStatus(Enum):
    """Статус объекта"""
    # todo: переделать на StrEnums
    draft = Value(1, help=u'Черновик')
    published = Value(2, help=u'Опубликовано')
    deactivated = Value(3, help=u'Деактивировано')
    refused = Value(4, help=u'Отклонено')
    deleted = Value(5, help=u'Удалено')
    sold = Value(6, help=u'Продано')
    moderate = Value(7, help=u'Промодерировано')
    removed_by_moderator = Value(8, help=u'Удалено модератором')
    blocked = Value(9, help=u'Заблокировано')
