# pylint: skip-file
"""

Code generated by new-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client announcementapi`

new-codegen version: 4.0.0

"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Kp:
    """КП"""

    id: Optional[int] = None
    'ID коттеджного посёлка в базе CIAN<br />\r\nИдентификатор можно получить из url карточки коттеджного посёлка:<br /><img src="https://files.cian.ru/files/images/xml_import/doc_kpschema_id.png" width="415px" />'
    isResale: Optional[bool] = None
    """Признак вторичной недвижимости в КП"""