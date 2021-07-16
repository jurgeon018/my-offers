import pytest

from my_offers.enums import OfferServices
from my_offers.repositories.monolith_cian_announcementapi.entities import PublishTerm, PublishTerms
from my_offers.repositories.monolith_cian_announcementapi.entities.publish_term import Services
from my_offers.services.mobile_offers.get_my_offers._prepare_offers import _parse_services


@pytest.mark.parametrize(
    ('terms', 'excepted'),
    (
        (PublishTerms(), []),
        (PublishTerms(terms=[PublishTerm()]), []),
        (PublishTerms(terms=[PublishTerm(services=[Services.paid])]), [OfferServices.paid]),
        (PublishTerms(terms=[PublishTerm(services=[Services.calltracking])]), []),
    )
)
def test_parse_services(terms, excepted):
    # act
    result = _parse_services(terms)

    # assert
    assert result == excepted
