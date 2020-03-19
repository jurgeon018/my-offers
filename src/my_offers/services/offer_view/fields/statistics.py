from my_offers import entities


def get_statistics(*, coverage: entities.Coverage, favorites: int) -> entities.Statistics:
    return entities.Statistics(
        shows=coverage.shows_count,
        views=coverage.searches_count,
        favorites=favorites,
    )
