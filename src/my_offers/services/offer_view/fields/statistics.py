from typing import Optional

from my_offers import entities


def get_statistics(*, coverage: Optional[entities.Coverage], favorites: Optional[int]) -> entities.Statistics:
    if coverage:
        return entities.Statistics(
            shows=coverage.shows_count,
            views=coverage.searches_count,
            favorites=favorites,
        )

    return entities.Statistics(
        shows=None,
        views=None,
        favorites=favorites,
    )
