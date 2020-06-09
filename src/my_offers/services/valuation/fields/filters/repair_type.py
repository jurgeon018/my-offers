from typing import Optional

from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import RepairType
from my_offers.repositories.price_estimator.entities import EstimationUserChosenFilters
from my_offers.repositories.price_estimator.entities.estimation_user_chosen_filters import Key, Value


REPAIR_TYPE_OBJECT_MODEL_VALUATION_FILTERS = {
    RepairType.no: Value.repair_type_without,
    RepairType.euro: Value.repair_type_euro,
    RepairType.design: Value.repair_type_design,
    RepairType.cosmetic: Value.repair_type_cosmetic,
}


def get_repair_type(
        repair_type: RepairType
) -> Optional[EstimationUserChosenFilters]:
    filters_repair_type = REPAIR_TYPE_OBJECT_MODEL_VALUATION_FILTERS.get(repair_type)

    if filters_repair_type:
        return EstimationUserChosenFilters(
            key=Key.repair_type,
            value=[filters_repair_type]
        )
    return None
