from datetime import timedelta

import pytest

from my_offers.repositories.monolith_cian_announcementapi.entities import PublishTerm, PublishTerms
from my_offers.repositories.monolith_cian_announcementapi.entities.publish_term import Services
from my_offers.services.offer_view.fields.publish_features import _get_remain, get_publish_features


@pytest.mark.parametrize(
    ('terms', 'expected'),
    (
        (None, []),
        (PublishTerms(autoprolong=False), []),
        (PublishTerms(autoprolong=True), ['автопродление']),
        (PublishTerms(autoprolong=True, terms=[PublishTerm(services=[Services.premium])]), ['автопродление']),
        (PublishTerms(autoprolong=False, terms=[PublishTerm(services=[Services.premium])]), []),
        (PublishTerms(autoprolong=True, terms=[PublishTerm(services=[Services.premium], days=1)]), []),
        (PublishTerms(autoprolong=True, terms=[PublishTerm(services=[Services.calltracking])]), ['автопродление']),
    ),
)
def test_get_publish_features(mocker, terms, expected):
    # arrange & act
    result = get_publish_features(publish_terms=terms, payed_remain=None)

    # assert
    assert result == expected


def test_get_publish_features__termless__termless(mocker):
    # arrange
    delta = timedelta(days=400)
    terms = PublishTerms(autoprolong=False)

    expected = ['бессрочно']

    # act
    result = get_publish_features(publish_terms=terms, payed_remain=delta)

    # assert
    assert result == expected


def test_get_publish_features__payed_remain__payed_remain(mocker):
    # arrange
    delta = timedelta(days=40)
    terms = PublishTerms(autoprolong=False)

    expected = ['осталось 40 д.']

    # act
    result = get_publish_features(publish_terms=terms, payed_remain=delta)

    # assert
    assert result == expected


@pytest.mark.parametrize(
    ('delta', 'expected'),
    (
        (timedelta(days=20), '20 д.'),
        (timedelta(minutes=61), '1 ч.'),
        (timedelta(minutes=10), '10 м.'),
    )
)
def test__get_remain(delta, expected):
    # arrange & act
    result = _get_remain(delta)

    # assert
    assert result == expected
