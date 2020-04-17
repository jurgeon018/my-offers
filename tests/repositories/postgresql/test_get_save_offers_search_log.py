from my_offers import pg
from my_offers.repositories.postgresql.offers_search_log import save_offers_search_log


async def test_save_offers_search_log():
    # act
    await save_offers_search_log(filters={'zz': 1}, found_cnt=10, is_error=False)

    # assert
    pg.get().execute.assert_called_once_with(
        'INSERT INTO offers_search_log VALUES($1, $2, $3)',
        '{"zz": 1}',
        10,
        False,
    )
