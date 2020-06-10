from typing import Optional

from my_offers.repositories.price_estimator.entities import EstimationUserChosenFilters
from my_offers.repositories.price_estimator.entities.estimation_user_chosen_filters import Key, Value


def get_floor(
        *,
        floor_number: Optional[int],
        building_floors_count: Optional[int],
) -> Optional[EstimationUserChosenFilters]:
    value = None

    if floor_number == 1:
        value = Value.floor_one
    elif floor_number == 2:
        value = Value.floor_two
    elif building_floors_count and floor_number == building_floors_count:
        value = Value.floor_last
    elif floor_number:
        value = Value.floor_other

    if value:
        return EstimationUserChosenFilters(
            key=Key.floor,
            value=[value],
        )
    return None
