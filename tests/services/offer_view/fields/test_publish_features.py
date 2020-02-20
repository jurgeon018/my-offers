import pytest

from my_offers.repositories.monolith_cian_announcementapi.entities import PublishTerm, PublishTerms
from my_offers.repositories.monolith_cian_announcementapi.entities.publish_term import Services
from my_offers.services.offer_view.fields.publish_features import get_publish_features


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
    result = get_publish_features(terms)

    # assert
    assert result == expected
