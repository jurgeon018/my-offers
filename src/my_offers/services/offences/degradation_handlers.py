from cian_core.degradation import get_degradation_handler

from ._get_offences import get_offers_with_image_offences, get_offers_with_video_offences
from .get_unidentified_offers import get_unidentified_offers


get_offers_with_image_offences_degradation_handler = get_degradation_handler(
    func=get_offers_with_image_offences,
    key='moderation.get_offers_with_image_offences',
    default=set(),
)

get_offers_with_video_offences_degradation_handler = get_degradation_handler(
    func=get_offers_with_video_offences,
    key='moderation.get_offers_with_video_offences',
    default=set(),
)

get_unidentified_offers_degradation_handler = get_degradation_handler(
    func=get_unidentified_offers,
    key='moderation_checks_orchestrator.get_unidentified_offers',
    default=[],
)
