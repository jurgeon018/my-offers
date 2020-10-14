from my_offers import entities, enums, pg
from my_offers.helpers.category import get_types
from my_offers.helpers.fields import get_sort_date
from my_offers.helpers.similar import is_offer_for_similar
from my_offers.repositories.monolith_cian_announcementapi.entities import ObjectModel
from my_offers.repositories.postgresql import offers_similars
from my_offers.repositories.postgresql.offers_duplicates import get_duplicate_group_id
from my_offers.services.convert_price import get_price_rur
from my_offers.services.similars.helpers.district import get_district_id
from my_offers.services.similars.helpers.house import get_house_id
from my_offers.services.similars.helpers.rooms_count import get_rooms_count
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

    similar = entities.OfferSimilar(
        offer_id=object_model.id,
        deal_type=deal_type,
        group_id=await get_duplicate_group_id(object_model.id),
        district_id=get_district_id(geo.district) if geo else None,
        house_id=get_house_id(geo.address) if geo else None,
        price=await get_price_rur(
            price=object_model.bargain_terms.price,
            currency=object_model.bargain_terms.currency
        ),
        rooms_count=get_rooms_count(
            rooms_count=object_model.rooms_count,
            rooms_for_sale_count=object_model.rooms_for_sale_count,
            flat_type=object_model.flat_type,
        ),
        sort_date=get_sort_date(object_model=object_model, status_tab=enums.OfferStatusTab.active),
    )

    conn = pg.get()
    async with conn.transaction():
        offer = await offers_similars.get_offer_similar_for_update(
            suffix=suffix,
            offer_id=similar.offer_id
        )

        if not offer:
            await offers_similars.insert_similar(
                suffix=suffix,
                similar=similar
            )
        else:
            if offer.price != similar.price:
                similar.old_price = offer.price

            await offers_similars.update_similar(
                suffix=suffix,
                similar=similar
            )
