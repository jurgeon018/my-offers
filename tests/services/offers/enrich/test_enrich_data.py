from datetime import datetime
from unittest import mock

import pytest
import pytz
from cian_test_utils import v
from simple_settings.utils import settings_stub

from my_offers import enums
from my_offers.entities import AgentHierarchyData
from my_offers.entities.enrich import AddressUrlParams
from my_offers.entities.offer_relevance_warning import OfferRelevanceWarningInfo
from my_offers.entities.offer_view_model import Subagent
from my_offers.repositories.monolith_cian_announcementapi.entities import AddressInfo, address_info
from my_offers.services.offers.enrich.enrich_data import AddressUrls, EnrichData, EnrichParams


def test_get_geo_url_params(mocker):
    # arrange
    params = EnrichParams(111)
    params.add_geo_url_id(
        deal_type=enums.DealType.rent,
        offer_type=enums.OfferType.flat,
        geo_type=address_info.Type.underground,
        geo_id=11
    )

    expected = [
        AddressUrlParams(
            deal_type=enums.DealType.rent,
            offer_type=enums.OfferType.flat,
            address_info=[
                AddressInfo(
                    id=11,
                    type=address_info.Type.underground
                )
            ]
        )
    ]

    # act
    result = params.get_geo_url_params()

    # assert
    assert result == expected


def test_address_urls__none__none(mocker):
    # arrange
    urls = AddressUrls()
    address = AddressInfo(id=11, type=address_info.Type.underground)

    # act
    result = urls.get_url(address)

    # assert
    assert result is None


def test_enrich_data__get_offer_offence__moderation_info_is_none(mocker):
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
        moderation_info=None
    )

    # act
    result = enrich_data.get_offer_offence(offer_id=111)

    # assert
    assert result is None


@pytest.mark.parametrize('moderation_info, expected', [
    ({}, None),
    ({111: mock.sentinel.offer_offence}, mock.sentinel.offer_offence),
])
def test_enrich_data__get_offer_offence(mocker, moderation_info, expected):
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
        moderation_info=moderation_info
    )

    # act
    result = enrich_data.get_offer_offence(offer_id=111)

    # assert
    assert result == expected


@pytest.mark.parametrize(
    ('user_id', 'expected'),
    (
        (12, Subagent(id=12, name='Zz Mm')),
        (14, None),
    )
)
def test_get_subagent(mocker, user_id, expected):
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
        subagents={12: Subagent(id=12, name='Zz Mm')}
    )

    # act
    result = enrich_data.get_subagent(user_id)

    # assert
    assert result == expected


def test_get_subagent__none__none(mocker):
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
    result = enrich_data.get_subagent(12)

    # assert
    assert result is None


@pytest.mark.parametrize(
    ('offer_id', 'expected'),
    (
        (12, True),
        (14, False),
    )
)
def test_on_premoderation(mocker, offer_id, expected):
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
        premoderation_info={12, 55}
    )

    # act
    result = enrich_data.on_premoderation(offer_id)

    # assert
    assert result == expected


@pytest.mark.gen_test
@pytest.mark.parametrize(
    ('offer_id', 'expected'),
    (
        (1, datetime(2020, 4, 29, tzinfo=pytz.UTC)),
        (4, None),
    )
)
async def test_get_archive_date(mocker, offer_id, expected):
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
        archive_date={1: datetime(2020, 3, 30, tzinfo=pytz.UTC)}
    )

    # act
    with settings_stub(DAYS_BEFORE_ARCHIVATION=30):
        result = enrich_data.get_archive_date(offer_id)

    # assert
    assert result == expected


@pytest.mark.gen_test
@pytest.mark.parametrize(
    ('offer_id', 'expected'),
    (
        (1, datetime(2020, 4, 29, tzinfo=pytz.UTC)),
        (4, None),
    )
)
async def test_get_payed_till(mocker, offer_id, expected):
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
        payed_till={1: datetime(2020, 4, 29, tzinfo=pytz.UTC)}
    )

    # act
    result = enrich_data.get_payed_till(offer_id)

    # assert
    assert result == expected


@pytest.mark.parametrize(
    ('offer_id', 'expected'),
    (
        (
            1,
            v(OfferRelevanceWarningInfo(
                offer_id=1,
                check_id='foo',
            ))
        ),
        (4, None),
    )
)
def test_offer_relevance_warning(mocker, offer_id, expected):
    # arrange
    enrich_data = EnrichData(
        agent_hierarchy_data=AgentHierarchyData(
            is_master_agent=False,
            is_sub_agent=False,
        ),
        offer_relevance_warnings={
            1: v(OfferRelevanceWarningInfo(
                offer_id=1,
                check_id='foo',
            ))
        }
    )

    # act
    result = enrich_data.get_offer_relevance_warning(offer_id)

    # assert
    assert result == expected
