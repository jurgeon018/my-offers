from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Category


CATEGORY_FOR_VALUATION = (
    Category.flat_sale,
    Category.room_sale,
    Category.flat_rent,
    Category.room_rent,
)


def validate_offer(category: Category) -> bool:
    return category in CATEGORY_FOR_VALUATION
