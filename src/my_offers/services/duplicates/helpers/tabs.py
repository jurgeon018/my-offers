from typing import List

from my_offers import entities, enums


def get_tabs(total_count: int) -> List[entities.Tab]:
    return [
        entities.Tab(
            type=enums.DuplicateTabType.all,
            title='Все',
            count=total_count,
        )
    ]
