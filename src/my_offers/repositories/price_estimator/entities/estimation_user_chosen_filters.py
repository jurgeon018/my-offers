# pylint: skip-file
"""

Code generated by cian-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client price-estimator`

cian-codegen version: 1.4.3

"""
from dataclasses import dataclass
from typing import List

from cian_enum import NoFormat, StrEnum


class Key(StrEnum):
    __value_format__ = NoFormat
    amenities = 'amenities'
    """Удобства"""
    entrance = 'entrance'
    """Подъезд"""
    floor = 'floor'
    """Этаж"""
    living_conditions = 'livingConditions'
    """Условия проживания"""
    repair_age = 'repairAge'
    """Сколько лет ремонту?"""
    repair_type = 'repairType'
    """Укажите тип ремонта?"""


class Value(StrEnum):
    __value_format__ = NoFormat
    children_allowed = 'childrenAllowed'
    """Можно с детьми"""
    conditioner = 'conditioner'
    """Кондиционер"""
    entrance_after_repair = 'entranceAfterRepair'
    """Парадная после ремонта"""
    entrance_concierge = 'entranceConcierge'
    """Есть консьерж в парадной"""
    floor_last = 'floorLast'
    """Последний этаж"""
    floor_one = 'floorOne'
    """1 этаж"""
    floor_other = 'floorOther'
    """Другой этаж"""
    floor_two = 'floorTwo'
    """2 этаж"""
    fridge = 'fridge'
    """Холодильник"""
    kitchen_furniture = 'kitchenFurniture'
    """Кухонная мебель"""
    pets_allowed = 'petsAllowed'
    """Можно с животными"""
    repair_age_four = 'repairAgeFour'
    """4 года ремонту"""
    repair_age_more_than_five = 'repairAgeMoreThanFive'
    """Больше 5 лет ремонту"""
    repair_age_one = 'repairAgeOne'
    """1 год ремонту"""
    repair_age_three = 'repairAgeThree'
    """3 года ремонту"""
    repair_age_two = 'repairAgeTwo'
    """2 года ремонту"""
    repair_type_cosmetic = 'repairTypeCosmetic'
    """Косметический ремонт"""
    repair_type_design = 'repairTypeDesign'
    """Дизайнерский ремонт"""
    repair_type_euro = 'repairTypeEuro'
    """Евроремонт"""
    repair_type_without = 'repairTypeWithout'
    """Без ремонта"""
    tv = 'tv'
    """Телевизор"""
    washing_machine = 'washingMachine'
    """Стиральная машина"""


@dataclass
class EstimationUserChosenFilters:
    key: Key
    """Имя фильтра"""
    value: List[Value]
    """Выбранные(ое) значения(е)"""
