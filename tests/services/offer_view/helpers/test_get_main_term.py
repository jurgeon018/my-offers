import pytest

from my_offers.repositories.monolith_cian_announcementapi.entities import PublishTerm
from my_offers.repositories.monolith_cian_announcementapi.entities.publish_term import Services
from my_offers.services.offer_view.helpers.terms import get_main_term


@pytest.mark.parametrize(
    ('terms', 'expected'),
    (
        (None, None),
        ([PublishTerm(services=[])], None),
        ([PublishTerm(services=[Services.calltracking])], None),
        ([PublishTerm(services=[Services.premium])], PublishTerm(services=[Services.premium])),
        (
            [
                PublishTerm(services=[Services.top3]),
                PublishTerm(services=[Services.calltracking]),
            ],
            PublishTerm(services=[Services.top3])
        ),
    )
)
def test_get_main_term(mocker, terms, expected):

    # arrange & act
    result = get_main_term(terms)

    # assert
    assert result == expected
