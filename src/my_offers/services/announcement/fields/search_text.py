import logging
import re
from typing import List, Optional, Union, Pattern

from my_offers.helpers.title import get_title
from my_offers.repositories.monolith_cian_announcementapi.entities import (
    AddressInfo,
    DistrictInfo,
    HighwayInfo,
    ObjectModel,
    RailwayInfo,
    UndergroundInfo,
)


logger = logging.getLogger(__name__)


HOME_PATTERN: Pattern = re.compile(r'(([двлкс]+)([\d\/]+[^кс]?))', re.IGNORECASE)


def get_search_text(object_model: ObjectModel) -> str:
    result = [str(object_model.id)]  # ID объявления

    # Номер телефона в объявлении (оригинальный): независимо от того, как ты вводишь номер телефона,
    # убираются все знаки препинания и пробелы и ищется последовательность цифр.
    for phone in object_model.phones:
        # TODO: https://jira.cian.tech/browse/CD-77625
        if phone.number:
            result.append(phone.number)
        if source_phone := phone.source_phone:
            result.append(source_phone.number)

    if geo := object_model.geo:
        if address := geo.user_input:
            result.append(address)

        result += _collect_names(geo.address)       # Адрес (город, улица, дом)
        result += _get_house(geo.address)           # доп. варианты для дома
        result += _collect_names(geo.undergrounds)  # Метро
        result += _collect_names(geo.district)      # Район
        result += _collect_names(geo.highways)      # Шоссе
        result += _collect_names(geo.railways)      # Жд

        if jk := geo.jk:                            # ЖК
            result.append(jk.name)

    # Заголовок
    # количество комнат: 1, 2, 3, 4, 5, 6+, студия, свободная планировка
    # тип: квартира, апартаменты, комната, доля, дом, часть дома, таунхаус, участок, офис и т.д.
    result.append(get_title(object_model))
    if object_model.title:
        result.append(object_model.title)

    # этаж раздельно
    if floor_number := object_model.floor_number:
        result.append(str(floor_number))
    if floors_count := object_model.building and object_model.building.floors_count:
        result.append(str(floors_count))

    # Текст на карточке объявления
    # Описание
    if object_model.description:
        result.append(object_model.description)

    return ' '.join(result)


def _collect_names(
        geo_items: Optional[List[Union[AddressInfo, DistrictInfo, HighwayInfo, RailwayInfo, UndergroundInfo]]]
) -> List[str]:
    if not geo_items:
        return []

    return [item.name for item in geo_items]


def _get_house(address: Optional[List[AddressInfo]]) -> List[str]:
    """
    по запросу "д7" должны находить "д7"
    по запросу "7д" должны находить "д7"
    """
    result: List[str] = []
    if not address:
        return result

    for item in address:
        if item.type and item.type.is_house:
            if house := item.name:
                if not house.startswith('вл'):
                    house = 'д' + house
                if parts := re.findall(HOME_PATTERN, house):
                    for part in parts:
                        result += part
                        result.append(part[2] + part[1])
                else:
                    logger.warning('Cant parse house: %s', house)
            break

    return result
