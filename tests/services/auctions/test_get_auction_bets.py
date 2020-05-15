from cian_test_utils import future

from my_offers.repositories.auction.entities import (
    AnnouncementsBetModel,
    AnnouncementsBetResponse,
    GetAnnouncementsBetsRequest,
)
from my_offers.services.auctions._get_auction_bets import get_auction_bets


async def test_get_auction_bets(mocker):
    # arrange
    request = GetAnnouncementsBetsRequest(announcements_ids=[1, 2])
    expected = {1: 12.0}
    v1_get_bets_by_announcements_mock = mocker.patch(
        'my_offers.services.auctions._get_auction_bets.v1_get_bets_by_announcements',
        return_value=future(AnnouncementsBetResponse(
            bets=[
                AnnouncementsBetModel(announcement_id=1, bet=12.0)
            ]
        ))
    )

    # act
    result = await get_auction_bets([1, 2])

    # arrange
    assert result == expected
    v1_get_bets_by_announcements_mock.assert_called_once_with(request)


async def test_get_auction_bets__empty__empty(mocker):
    # arrange
    request = GetAnnouncementsBetsRequest(announcements_ids=[1, 2])
    expected = {}
    v1_get_bets_by_announcements_mock = mocker.patch(
        'my_offers.services.auctions._get_auction_bets.v1_get_bets_by_announcements',
        return_value=future(AnnouncementsBetResponse())
    )

    # act
    result = await get_auction_bets([1, 2])

    # arrange
    assert result == expected
    v1_get_bets_by_announcements_mock.assert_called_once_with(request)
