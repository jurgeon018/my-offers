from my_offers import entities
from my_offers.helpers.category import get_types
from my_offers.helpers.similar import is_offer_for_similar
from my_offers.repositories.monolith_cian_announcementapi.entities import ObjectModel
from my_offers.repositories.postgresql import offers_similars
from my_offers.repositories.postgresql.offers_duplicates import get_duplicate_group_id
from my_offers.services.announcement.fields.district_id import get_district_id
from my_offers.services.announcement.fields.house_id import get_house_id
from my_offers.services.convert_price import get_price_rur
from my_offers.services.similars.helpers.table import get_similar_table_suffix


async def update(object_model: ObjectModel) -> None:
    suffix = get_similar_table_suffix(object_model)

    if is_offer_for_similar(status=object_model.status, category=object_model.category):
        await _save(suffix=suffix, object_model=object_model)
    else:
        await offers_similars.delete(suffix=suffix, offer_id=object_model.id)


async def _save(*, suffix: str, object_model: ObjectModel) -> None:
    _, deal_type = get_types(object_model.category)
    geo = object_model.geo

    await offers_similars.save(
        suffix=suffix,
        similar=entities.OfferSimilar(
            offer_id=object_model.id,
            deal_type=deal_type,
            group_id=await get_duplicate_group_id(object_model.id),
            district_id=get_district_id(geo.district) if geo else None,
            house_id=get_house_id(geo.address) if geo else None,
            price=await get_price_rur(
                price=object_model.bargain_terms.price,
                currency=object_model.bargain_terms.currency
            ),
            rooms_count=object_model.rooms_count,
            sort_date=object_model.edit_date if object_model.edit_date else object_model.creation_date,
        )
    )
