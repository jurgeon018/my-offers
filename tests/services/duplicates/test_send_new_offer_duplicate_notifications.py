from cian_test_utils import future

from my_offers.repositories.monolith_cian_announcementapi.entities import BargainTerms, ObjectModel, Phone
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Category, Status
from my_offers.services.duplicates import send_new_offer_duplicate_notifications


PATH = 'my_offers.services.duplicates._send_new_offer_duplicate_notifications.'


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
                    )
                ],
                1
            )),
            future((
                [],
                1,
            ))
        ]
    )

    # act
    await send_new_offer_duplicate_notifications(1)

    # assert
    get_object_model_mock.assert_called_once_with({'offer_id': 1})
    get_offer_duplicates_mock.assert_has_calls([
        mocker.call(limit=100, offer_id=1, offset=0),
        mocker.call(limit=100, offer_id=1, offset=100),
    ])
