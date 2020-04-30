from typing import Optional

from my_offers import entities


def get_statistics(*, views: Optional[int], searches: Optional[int], favorites: Optional[int]) -> entities.Statistics:
    return entities.Statistics(
        shows=searches,  # Количество показов в поиске == Количество поисков
        views=views,  # Количество просмотров карточки == Количество показов
        favorites=favorites,
    )
