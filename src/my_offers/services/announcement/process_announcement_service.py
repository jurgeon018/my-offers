from datetime import datetime

from my_offers import entities
from my_offers.helpers.category import get_types
from my_offers.helpers.fields import get_sort_date, is_archived
from my_offers.helpers.status_tab import get_status_tab
from my_offers.mappers.object_model import object_model_mapper
from my_offers.repositories import postgresql
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import ObjectModel
from my_offers.repositories.postgresql.billing import get_offer_publisher_user_id
from my_offers.services.announcement.fields.district_id import get_district_id
from my_offers.services.announcement.fields.house_id import get_house_id
from my_offers.services.announcement.fields.is_test import get_is_test
from my_offers.services.announcement.fields.prices import get_prices
from my_offers.services.announcement.fields.search_text import get_search_text
from my_offers.services.announcement.fields.services import get_services
from my_offers.services.announcement.fields.street_name import get_street_name
from my_offers.services.announcement.fields.total_area import get_total_area
from my_offers.services.announcement.fields.walking_time import get_walking_time


async def process_announcement(object_model: ObjectModel, event_date: datetime) -> None:
    offer = await prepare_offer(object_model)

    if is_archived(flags=object_model.flags):
        await postgresql.save_offer_archive(offer=offer, event_date=event_date)
    else:
        await postgresql.save_offer(offer=offer, event_date=event_date)

    await post_process_announcement(object_model)


async def prepare_offer(object_model: ObjectModel) -> entities.Offer:
    offer_type, deal_type = get_types(object_model.category)
    status_tab = get_status_tab(
        offer_flags=object_model.flags,
        offer_status=object_model.status,
    )
    total_area = get_total_area(total_area=object_model.total_area, land=object_model.land)
    price, price_per_meter = get_prices(bargain_terms=object_model.bargain_terms, total_area=total_area)
    geo = object_model.geo
    offer = entities.Offer(
        offer_id=object_model.id,
        master_user_id=await _get_master_user_id(offer_id=object_model.id, user_id=object_model.user_id),
        user_id=object_model.published_user_id,
        deal_type=deal_type,
        offer_type=offer_type,
        status_tab=status_tab,
        search_text=get_search_text(object_model),
        row_version=object_model.row_version,
        raw_data=object_model_mapper.map_to(object_model),
        services=get_services(object_model.publish_terms),
        is_manual=not (object_model.source and object_model.source.is_upload),
        is_in_hidden_base=bool(object_model.is_in_hidden_base),
        has_photo=bool(object_model.photos),
        is_test=get_is_test(object_model),
        price=price,
        price_per_meter=price_per_meter,
        total_area=total_area,
        walking_time=get_walking_time(geo),
        street_name=get_street_name(geo.address) if geo else None,
        sort_date=get_sort_date(object_model=object_model, status_tab=status_tab),
        district_id=get_district_id(geo.district) if geo else None,
        house_id=get_house_id(geo.address) if geo else None,
    )

    return offer


async def post_process_announcement(object_model: ObjectModel) -> None:
    if not object_model.status.is_draft:
        await postgresql.delete_offer_import_error(object_model.id)


async def _get_master_user_id(*, offer_id: int, user_id: int) -> int:
    publisher_user_id = await get_offer_publisher_user_id(offer_id)

    return publisher_user_id if publisher_user_id else user_id
