from datetime import datetime

from cian_test_utils import future

from my_offers import enums
from my_offers.entities import OfferSimilar
from my_offers.enums import DuplicateType
from my_offers.repositories.monolith_cian_announcementapi.entities import BargainTerms, ObjectModel, Phone
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Category, Status
from my_offers.services.duplicates import send_new_duplicate_notifications
from my_offers.services.duplicates.send_duplicate_notifications import send_duplicate_price_changed_notifications


PATH = 'my_offers.services.duplicates.send_duplicate_notifications.'


async def test_send_new_offer_duplicate_notifications__owner__skip(mocker):
    # arrange
    get_object_model_mock = mocker.patch(
        f'{PATH}get_object_model',
        return_value=future(
            ObjectModel(
                id=111,
                bargain_terms=BargainTerms(price=123),
                category=Category.office_sale,
                phones=[Phone(country_code='1', number='12312')],
                user_id=222,
                total_area=100,
                can_parts=True,
                min_area=7,
                status=Status.published,
            )
        )
    )

    get_offer_duplicates_mock = mocker.patch(
        f'{PATH}get_offer_duplicates',
        side_effect=[
            future((
                [
                    ObjectModel(
                        id=222,
                        bargain_terms=BargainTerms(price=123),
                        category=Category.office_sale,
                        phones=[Phone(country_code='1', number='12312')],
                        user_id=222,
                        total_area=100,
                        can_parts=True,
                        min_area=7,
                    ),
                    DuplicateType.duplicate
                ],
            )),
            future((
                []
            ))
        ]
    )
    send_new_duplicates_notification_mock = mocker.patch(
        f'{PATH}send_new_duplicates_notification',
        return_value=future()
    )

    # act
    await send_new_duplicate_notifications(duplicate_offer_id=1)

    # assert
    get_object_model_mock.assert_called_once_with({'offer_id': 1})
    get_offer_duplicates_mock.assert_has_calls([
        mocker.call(limit=100, offer_id=1, offset=0),
        mocker.call(limit=100, offer_id=1, offset=100),
    ])
    send_new_duplicates_notification_mock.assert_not_called()


async def test_send_duplicate_price_changed_notifications__owner__skip(mocker):
    # arrange
    get_object_model_mock = mocker.patch(
        f'{PATH}get_object_model',
        return_value=future(
            ObjectModel(
                id=111,
                bargain_terms=BargainTerms(price=123),
                category=Category.office_sale,
                phones=[Phone(country_code='1', number='12312')],
                user_id=222,
                total_area=100,
                can_parts=True,
                min_area=7,
                status=Status.published,
            )
        )
    )

    get_offer_duplicates_mock = mocker.patch(
        f'{PATH}get_offer_duplicates',
        side_effect=[
            future((
                [
                    ObjectModel(
                        id=222,
                        bargain_terms=BargainTerms(price=123),
                        category=Category.office_sale,
                        phones=[Phone(country_code='1', number='12312')],
                        user_id=222,
                        total_area=100,
                        can_parts=True,
                        min_area=7,
                    ),
                    DuplicateType.duplicate
                ],
            )),
            future((
                []
            ))
        ]
    )
    send_duplicate_price_changed_mobile_push_mock = mocker.patch(
        f'{PATH}send_duplicate_price_changed_mobile_push',
        return_value=future()
    )
    mocker.patch(
        f'{PATH}get_offer_similar',
        return_value=future(OfferSimilar(
            offer_id=1,
            deal_type=enums.DealType.rent,
            sort_date=datetime.now(),
            group_id=None,
            district_id=None,
            house_id=None,
            rooms_count=None,
            price=1000000,
            old_price=1100000,
        ))
    )

    # act
    await send_duplicate_price_changed_notifications(duplicate_offer_id=1)

    # assert
    get_object_model_mock.assert_called_once_with({'offer_id': 1})
    get_offer_duplicates_mock.assert_has_calls([
        mocker.call(limit=100, offer_id=1, offset=0),
        mocker.call(limit=100, offer_id=1, offset=100),
    ])
    send_duplicate_price_changed_mobile_push_mock.assert_not_called()


async def test_send_duplicate_price_changed_notifications__not_found_duplicate(mocker):
    # arrange
    get_object_model_mock = mocker.patch(
        f'{PATH}get_object_model',
        return_value=future(None)
    )
    send_duplicate_price_changed_mobile_push_mock = mocker.patch(
        f'{PATH}send_duplicate_price_changed_mobile_push',
        return_value=future()
    )
    get_offer_duplicates_mock = mocker.patch(
        f'{PATH}get_offer_duplicates',
        return_value=future(None)
    )

    # act
    await send_duplicate_price_changed_notifications(duplicate_offer_id=1)

    # assert
    get_object_model_mock.assert_called_once_with({'offer_id': 1})
    get_offer_duplicates_mock.assert_not_called()
    send_duplicate_price_changed_mobile_push_mock.assert_not_called()


async def test_send_duplicate_price_changed_notifications__not_found_similar(mocker):
    # arrange
    get_object_model_mock = mocker.patch(
        f'{PATH}get_object_model',
        return_value=future(
            ObjectModel(
                id=111,
                bargain_terms=BargainTerms(price=123),
                category=Category.office_sale,
                phones=[Phone(country_code='1', number='12312')],
                user_id=222,
                total_area=100,
                can_parts=True,
                min_area=7,
                status=Status.published,
            )
        )
    )
    send_duplicate_price_changed_mobile_push_mock = mocker.patch(
        f'{PATH}send_duplicate_price_changed_mobile_push',
        return_value=future()
    )
    mocker.patch(
        f'{PATH}get_offer_similar',
        return_value=future(None)
    )
    get_offer_duplicates_mock = mocker.patch(
        f'{PATH}get_offer_duplicates',
        return_value=future(None)
    )

    # act
    await send_duplicate_price_changed_notifications(duplicate_offer_id=1)

    # assert
    get_object_model_mock.assert_called_once_with({'offer_id': 1})
    get_offer_duplicates_mock.assert_not_called()
    send_duplicate_price_changed_mobile_push_mock.assert_not_called()
