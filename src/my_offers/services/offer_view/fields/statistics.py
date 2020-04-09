from typing import Optional

from my_offers import entities


def get_statistics(*, coverage: Optional[entities.Coverage], favorites: Optional[int]) -> entities.Statistics:
    if coverage:
        return entities.Statistics(
            shows=coverage.searches_count,  # Количество показов в поиске == Количество поисков
            views=coverage.shows_count,  # Количество просмотров карточки == Количество показов
            favorites=favorites,
        )

    return entities.Statistics(
        shows=None,
        views=None,
        favorites=favorites,
    )
