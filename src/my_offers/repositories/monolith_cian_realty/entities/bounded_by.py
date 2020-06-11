# pylint: skip-file
"""

Code generated by cian-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client monolith-cian-realty`

cian-codegen version: 1.4.3

"""
from dataclasses import dataclass
from typing import Optional

from .bounded_by_corner import BoundedByCorner


@dataclass
class BoundedBy:
    'Согласно общепринятым названиям https://tech.yandex.ru/maps/doc/ymapsml/1.x/ref/reference/gml-boundedBy-docpage/\r\nОбласть показа для большинства геообъектов - это минимальный прямоугольник, который можно описать вокруг объекта. \r\nОбласть задается двумя геоточками, координаты которых содержатся в тегах lowerCorner и upperCorner.'
    lower_corner: Optional[BoundedByCorner] = None
    upper_corner: Optional[BoundedByCorner] = None
