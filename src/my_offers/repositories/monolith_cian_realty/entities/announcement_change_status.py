# pylint: skip-file
"""

Code generated by cian-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client monolith-cian-realty`

cian-codegen version: 1.4.3

"""
from dataclasses import dataclass
from typing import Optional

from cian_enum import NoFormat, StrEnum


class AnnouncementType(StrEnum):
    __value_format__ = NoFormat
    flat = 'Flat'
    """Городская недвижимость - Квартира аренда"""
    flat2 = 'Flat2'
    """Городская недвижимость - Квартира продажа"""
    suburbian = 'Suburbian'
    """Загородная недвижимость и земля"""
    office = 'Office'
    """Коммерческая недвижимость - офисы и прочее"""


@dataclass
class AnnouncementChangeStatus:
    '    Запрос для изменения статуса объявления.<br />\r\n    Если заполнено поле {RealtyDmir.App.Announcements.Models.AnnouncementChangeStatus.RealtyObjectId}, будет использоваться оно, иначе должны быть заполнены поля \r\n{RealtyDmir.App.Announcements.Models.AnnouncementChangeStatus.CianAnnouncementId} и {RealtyDmir.App.Announcements.Models.AnnouncementChangeStatus.AnnouncementType}.<br />\r\n    Для изменения статуса объявления в архиве, должно быть заполнено поле {RealtyDmir.App.Announcements.Models.AnnouncementChangeStatus.RealtyObjectId}.'
    announcement_type: Optional[AnnouncementType] = None
    cian_announcement_id: Optional[int] = None
    """Id объявления в Циане."""
    cian_user_id: Optional[int] = None
    realty_object_id: Optional[int] = None
    """Realty Id объявления."""
