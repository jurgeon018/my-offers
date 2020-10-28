from cian_core.degradation import get_degradation_handler

from my_offers.enums.ab_group import DuplicatePriceChangedMobilePushExperiment, Experiments
from my_offers.repositories.ab_use import v1_get_experiment
from my_offers.repositories.ab_use.entities import V1GetExperiment
from my_offers.repositories.ab_use.entities.v1_get_experiment import Platform


v1_get_experiment_degradation_handler = get_degradation_handler(
    func=v1_get_experiment,
    key='v1_get_experiment',
    default=None
)


async def get_duplicate_price_changed_ab_group(
        user_id: int
) -> DuplicatePriceChangedMobilePushExperiment:
    result = await v1_get_experiment_degradation_handler(V1GetExperiment(
        experiment_name=Experiments.duplicate_price_changed_mobile_push.value,
        platform=Platform.backend,
        user_id=str(user_id),
    ))
    if result.value and (result.value.group_name == DuplicatePriceChangedMobilePushExperiment.experiment.value):
        return DuplicatePriceChangedMobilePushExperiment.experiment
    return DuplicatePriceChangedMobilePushExperiment.control
