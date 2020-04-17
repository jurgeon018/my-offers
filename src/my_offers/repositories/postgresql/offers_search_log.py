import json
from typing import Any, Dict

from my_offers import pg


async def save_offers_search_log(filters: Dict[str, Any], found_cnt: int, is_error: bool) -> None:
    query = 'INSERT INTO offers_search_log VALUES($1, $2, $3)'

    await pg.get().execute(query, json.dumps(filters), found_cnt, is_error)
