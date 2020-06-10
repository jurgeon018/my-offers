from typing import Optional

from my_offers.repositories.price_estimator.entities import EstimationUserChosenFilters
from my_offers.repositories.price_estimator.entities.estimation_user_chosen_filters import Key, Value


def get_amenities(
        *,
        kitchen_furniture: bool,
        washer: bool,
        tv: bool,
        fridge: bool,
        conditioner: bool,
) -> Optional[EstimationUserChosenFilters]:
    values = []

    if kitchen_furniture:
        values.append(Value.kitchen_furniture)
    if washer:
        values.append(Value.washing_machine)
    if tv:
        values.append(Value.tv)
    if fridge:
        values.append(Value.fridge)
    if conditioner:
        values.append(Value.conditioner)

    if values:
        return EstimationUserChosenFilters(
            key=Key.amenities,
            value=values,
        )
    return None
