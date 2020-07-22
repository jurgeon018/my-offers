from typing import List

from my_offers import entities, enums


def get_tabs(
        *,
        duplicate_count: int,
        same_building_count: int,
        similar_count: int,
) -> List[entities.Tab]:
    tabs = []
    total_count = duplicate_count + same_building_count + similar_count
    if total_count:
        tabs.append(
            entities.Tab(
                type=enums.DuplicateTabType.all,
                title='Все',
                count=total_count,
            )
        )
    if duplicate_count:
        tabs.append(
            entities.Tab(
                type=enums.DuplicateTabType.duplicate,
                title='Дубли',
                count=duplicate_count,
            )
        )
    if same_building_count:
        tabs.append(
            entities.Tab(
                type=enums.DuplicateTabType.same_building,
                title='В этом доме',
                count=same_building_count,
            )
        )
    if similar_count:
        tabs.append(
            entities.Tab(
                type=enums.DuplicateTabType.similar,
                title='Похожие рядом',
                count=similar_count,
            )
        )
    return tabs
