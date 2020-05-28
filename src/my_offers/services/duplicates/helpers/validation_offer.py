from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Category, Status


CATEGORY_FOR_DUPLICATE = (
    Category.flat_sale,
    Category.room_sale,
    Category.flat_rent,
    Category.room_rent,
)


def validate_offer(*, status: Status, category: Category) -> bool:
    """
    Дубли делаем только для квартир и комнат во вторичке.
    Длительная аренда и продажа (без посуточной)
    """
    if not status.is_published:
        return False

    return category in CATEGORY_FOR_DUPLICATE
