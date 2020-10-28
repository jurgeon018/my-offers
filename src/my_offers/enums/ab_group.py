from cian_enum import NoFormat, StrEnum


class Experiments(StrEnum):
    __value_format__ = NoFormat
    duplicate_price_changed_mobile_push = 'duplicate_price_сhanged_mobile_push'


class DuplicatePriceChangedMobilePushExperiment(StrEnum):
    __value_format__ = NoFormat
    control = 'control'
    """Контрольная группа, в заголовке пуша нет цены"""
    experiment = 'experiment'
    """Экспериментальная группа, в заголовке пуша есть цена"""
