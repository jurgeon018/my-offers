from cian_core.degradation import get_degradation_handler

from .get_offers_with_offences import get_offers_with_media_offences
from .get_unidentified_offers import get_unidentified_offers


get_offers_with_media_offences_degradation_handler = get_degradation_handler(
    func=get_offers_with_media_offences,
    key='moderation.get_media_offences',
    default=([], []),
)

get_unidentified_offers_degradation_handler = get_degradation_handler(
    func=get_unidentified_offers,
    key='moderation_checks_orchestrator.get_unidentified_offers',
    default=[],
)
