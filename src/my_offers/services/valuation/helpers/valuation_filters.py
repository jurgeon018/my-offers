from typing import List, Optional

from my_offers.repositories.monolith_cian_announcementapi.entities import ObjectModel
from my_offers.repositories.price_estimator.entities import EstimationUserChosenFilters
from my_offers.services.valuation.fields.filters.amenities import get_amenities
from my_offers.services.valuation.fields.filters.floor import get_floor
from my_offers.services.valuation.fields.filters.living_сonditions import get_living_conditions
from my_offers.services.valuation.fields.filters.repair_type import get_repair_type


def get_valuation_filters(
        object_model: ObjectModel
) -> Optional[List[EstimationUserChosenFilters]]:
    result = []

    floor = get_floor(
        floor_number=object_model.floor_number,
        building_floors_count=object_model.building.floors_count if object_model.building else None
    )
    amenties = get_amenities(
        kitchen_furniture=object_model.has_kitchen_furniture,
        washer=object_model.has_washer,
        tv=object_model.has_tv,
        fridge=object_model.has_fridge,
        conditioner=object_model.has_conditioner,
    )
    living_conditions = get_living_conditions(
        children_allowed=object_model.children_allowed,
        pets_allowed=object_model.pets_allowed,
    )
    repair_type = get_repair_type(
        repair_type=object_model.repair_type
    )

    if floor:
        result.append(floor)
    if amenties:
        result.append(amenties)
    if living_conditions:
        result.append(living_conditions)
    if repair_type:
        result.append(repair_type)

    if result:
        return result
    return None
