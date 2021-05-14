import pytest

from my_offers.entities import AgentHierarchyData
from my_offers.entities.get_offers import ActiveInfo, DeclinedInfo, Moderation, NotActiveInfo, PageSpecificInfo
from my_offers.enums import OfferStatusTab
from my_offers.enums.not_active_status import NotActiveStatus
from my_offers.repositories.monolith_cian_announcementapi.entities import BargainTerms, ObjectModel, Phone
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Category, Status
from my_offers.services.offer_view.fields.page_specific_info import get_page_specific_info
from my_offers.services.offers.enrich.enrich_data import EnrichData


@pytest.mark.parametrize(
    ('object_model', 'status_tab', 'expected'),
    (
        (
            ObjectModel(
                id=111,
                bargain_terms=BargainTerms(price=123),
                category=Category.flat_rent,
                phones=[Phone(country_code='1', number='12312')],
                status=Status.published,
            ),
            OfferStatusTab.active,
            PageSpecificInfo(
                active_info=ActiveInfo(
                    vas=[],
                    is_from_package=False,
                    is_publication_time_ends=False,
                    publish_features=[],
                    auction=None
                ),
                not_active_info=None,
                declined_info=None
            ),
        ),
        (
            ObjectModel(
                id=111,
                bargain_terms=BargainTerms(price=123),
                category=Category.flat_rent,
                phones=[Phone(country_code='1', number='12312')],
                status=Status.draft,
            ),
            OfferStatusTab.not_active,
            PageSpecificInfo(
                active_info=None,
                not_active_info=NotActiveInfo(
                    status='Черновик',
                    message=None,
                    status_type=NotActiveStatus.discontinued
                ),
                declined_info=None
            ),
        ),
        (
            ObjectModel(
                id=111,
                bargain_terms=BargainTerms(price=123),
                category=Category.flat_rent,
                phones=[Phone(country_code='1', number='12312')],
                status=Status.blocked,
            ),
            OfferStatusTab.declined,
            PageSpecificInfo(
                active_info=None,
                not_active_info=None,
                declined_info=DeclinedInfo(
                    moderation=Moderation(
                        declined_date=None,
                        is_declined=False,
                        reason=None,
                        offence_status='Заблокировано'
                    )
                )
            )
        ),
    ),
)
def test_get_page_specific_info(object_model, status_tab, expected):
    # arrange
    enrich_data = EnrichData(
        agent_hierarchy_data=AgentHierarchyData(
            is_master_agent=False,
            is_sub_agent=False,
        ),
        auctions={},
        jk_urls={},
        geo_urls={},
        can_update_edit_dates={},
        import_errors={},
    )

    # act
    result = get_page_specific_info(object_model=object_model, enrich_data=enrich_data, status_tab=status_tab)

    # assert
    assert result == expected
