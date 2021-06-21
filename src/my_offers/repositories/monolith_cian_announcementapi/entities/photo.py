# pylint: skip-file
"""

Code generated by cian-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client monolith-cian-announcementapi`

cian-codegen version: 1.15.0

"""
from dataclasses import dataclass
from typing import Optional

from cian_enum import NoFormat, StrEnum

from .coordinates import Coordinates


class Source(StrEnum):
    __value_format__ = NoFormat
    camera = 'camera'
    """Снимок с камеры."""
    gallery = 'gallery'
    """Выбрано из галереи."""


@dataclass
class Photo:
    coordinates: Optional[Coordinates] = None
    """Координаты снимка."""
    full_url: Optional[str] = None
    """URL исходного изображения"""
    id: Optional[int] = None
    """ID фотографии"""
    is_cian_layout: Optional[bool] = None
    """Является ли фото планировкой Циан"""
    is_default: Optional[bool] = None
    """Является ли фото по-умолчанию"""
    mini_url: Optional[str] = None
    """URL превью"""
    rotate_degree: Optional[int] = None
    """Угол поворота"""
    source: Optional[Source] = None
    """Источник фото."""
    thumbnail2_url: Optional[str] = None
    """URL превью для мобильных приложений"""
    thumbnail_url: Optional[str] = None
    """URL превью"""
