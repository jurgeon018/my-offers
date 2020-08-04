from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Status, Category


CATEGORY_FOR_SIMILAR = (
    Category.flat_sale,
    Category.room_sale,
    Category.flat_rent,
    Category.room_rent,
)


def is_offer_for_similar(*, status: Status, category: Category) -> bool:
    """
    Дубли делаем только для квартир и комнат во вторичке.
    Длительная аренда и продажа (без посуточной)
    """
    if not status.is_published:
        return False

    return category in CATEGORY_FOR_SIMILAR
