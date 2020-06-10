from typing import Optional

from my_offers.repositories.price_estimator.entities import EstimationUserChosenFilters
from my_offers.repositories.price_estimator.entities.estimation_user_chosen_filters import Key, Value


def get_living_conditions(
        *,
        children_allowed: bool,
        pets_allowed: bool,
) -> Optional[EstimationUserChosenFilters]:
    values = []

    if children_allowed:
        values.append(Value.children_allowed)
    if pets_allowed:
        values.append(Value.pets_allowed)

    if values:
        return EstimationUserChosenFilters(
            key=Key.living_conditions,
            value=values,
        )
    return None
