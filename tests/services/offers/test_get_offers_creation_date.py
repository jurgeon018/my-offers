import pytest
from cian_test_utils import future

from my_offers import entities
from my_offers.services.offers import get_offers_creation_date


PATH = 'my_offers.services.offers._offers_creation_date.'


@pytest.mark.gen_test
async def test_get_offers_creation_date(mocker):
    # arrange
    get_offers_creation_date_mock = mocker.patch(
        f'{PATH}postgresql.get_offers_creation_date',
        return_value=future([entities.OfferCreationDate(offer_id=22, creation_date=None)])
    )
    request = entities.OffersCreationDateRequest(
        master_user_id=1,
        offer_ids=[22]
    )

    expected = entities.OffersCreationDateResponse(offers=[entities.OfferCreationDate(offer_id=22, creation_date=None)])

    # act
    result = await get_offers_creation_date(request)

    # assert
    assert result == expected
    get_offers_creation_date_mock.assert_called_once_with(master_user_id=1, offer_ids=[22])


@pytest.mark.gen_test
async def test_get_offers_creation_date__no_offers__empty(mocker):
    # arrange
    get_offers_creation_date_mock = mocker.patch(
        f'{PATH}postgresql.get_offers_creation_date',
        return_value=future([entities.OfferCreationDate(offer_id=22, creation_date=None)])
    )
    request = entities.OffersCreationDateRequest(
        master_user_id=1,
        offer_ids=[]
    )

    expected = entities.OffersCreationDateResponse(offers=[])

    # act
    result = await get_offers_creation_date(request)

    # assert
    assert result == expected
    get_offers_creation_date_mock.assert_not_called()
