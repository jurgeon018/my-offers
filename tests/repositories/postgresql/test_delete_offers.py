from cian_test_utils import future

from my_offers import pg
from my_offers.repositories.postgresql import delete_offers


async def test_delete_offers():
    # arrange
    pg.get().fetch.return_value = future([{'offer_id': 111}])

    # act
    result = await delete_offers([111], timeout=30)

    # assert
    assert result == [111]
