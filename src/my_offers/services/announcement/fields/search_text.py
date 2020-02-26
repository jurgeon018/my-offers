from typing import Dict

from my_offers.repositories.monolith_cian_announcementapi.entities import ObjectModel


def get_search_text(object_model: ObjectModel) -> str:
    result = [str(object_model.id)]
    if object_model.title:
        result.append(object_model.title)

    result.append(object_model.description)

    for phone in object_model.phones:
        if phone.country_code and phone.number:
            result.append(phone.country_code + phone.number)
        if source_phone := phone.source_phone:
            result.append(source_phone.country_code + source_phone.number)

    if geo := object_model.geo:
        if address := geo.user_input:
            result.append(address)

    if undergrounds := geo.undergrounds:
        for underground in undergrounds:
            result.append(underground.name)

    return ' '.join(result)
