from typing import Dict, List

from cian_core.degradation import get_degradation_handler

from my_offers.repositories.auction import v1_get_bets_by_announcements
from my_offers.repositories.auction.entities import GetAnnouncementsBetsRequest


async def get_auction_bets(offer_ids: List[int]) -> Dict[int, float]:
    response = await v1_get_bets_by_announcements(GetAnnouncementsBetsRequest(announcements_ids=offer_ids))
    if not response.bets:
        return {}

    return {bet.announcement_id: bet.bet for bet in response.bets}


get_auction_bets_degradation_handler = get_degradation_handler(
    func=get_auction_bets,
    key='get_auction_bets',
    default={},
)
