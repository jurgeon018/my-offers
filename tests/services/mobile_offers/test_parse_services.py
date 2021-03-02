import pytest

from my_offers.repositories.monolith_cian_announcementapi.entities import PublishTerms, PublishTerm
from my_offers.services.mobile_offers.get_my_offers._prepare_offers import _parse_services


@pytest.mark.parametrize(
    ('terms', 'excepted'),
    (
        (PublishTerms(), []),
        (PublishTerms(terms=[PublishTerm()]), []),
    )
)
def test_parse_services(terms, excepted):
    # act
    result = _parse_services(terms)

    # assert
    assert result == excepted
