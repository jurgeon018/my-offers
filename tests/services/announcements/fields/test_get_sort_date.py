from datetime import datetime

import pytest
import pytz

from my_offers.enums import OfferStatusTab
from my_offers.helpers.fields import get_sort_date
from my_offers.repositories.monolith_cian_announcementapi.entities import BargainTerms, ObjectModel, Phone
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Category


@pytest.mark.parametrize(
    ('object_model', 'status_tab', 'expected'),
    (
        (
            ObjectModel(
                id=111,
                bargain_terms=BargainTerms(price=123),
                category=Category.flat_rent,
                phones=[Phone(country_code='1', number='12312')],
                archived_date=datetime(2020, 2, 27, tzinfo=pytz.UTC),
            ),
            OfferStatusTab.archived,
            datetime(2020, 2, 27, tzinfo=pytz.UTC),
        ),
        (
            ObjectModel(
                id=111,
                bargain_terms=BargainTerms(price=123),
                category=Category.flat_rent,
                phones=[Phone(country_code='1', number='12312')],
                edit_date=datetime(2020, 2, 27, tzinfo=pytz.UTC),
            ),
            OfferStatusTab.active,
            datetime(2020, 2, 27, tzinfo=pytz.UTC),
        ),
        (
            ObjectModel(
                id=111,
                bargain_terms=BargainTerms(price=123),
                category=Category.flat_rent,
                phones=[Phone(country_code='1', number='12312')],
            ),
            OfferStatusTab.active,
            None,
        ),
    )
)
def test_get_sort_date(mocker, object_model, status_tab, expected):
    # arrange

    # act
    result = get_sort_date(object_model=object_model, status_tab=status_tab)

    # assert
    assert result == expected
