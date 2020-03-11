# pylint: skip-file
"""

Code generated by new-codegen; DO NOT EDIT.

To re-generate, run `new-codegen generate-client my-offers`

new-codegen version: 4.0.2

"""
from dataclasses import dataclass
from typing import List, Optional

from cian_enum import NoFormat, StrEnum

from .auction import Auction


class Vas(StrEnum):
    __value_format__ = NoFormat
    auction = 'auction'
    colorized = 'colorized'
    payed = 'payed'
    premium = 'premium'
    top3 = 'top3'


@dataclass
class ActiveInfo:
    isAutoprolong: bool
    """Автопродление"""
    isFromPackage: bool
    """ Флаг 'из пакета'"""
    isPublicationTimeEnds: bool
    """ Флаг 'меньше суток до конца публикации'"""
    vas: List[Vas]
    """Список VAS'ов"""
    auction: Optional[Auction] = None
    """Данные об аукционе по объявлению"""
    publishFeatures: Optional[List[str]] = None
    """Параметры публикации: сколько осталось"""
