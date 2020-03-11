import pytest

from my_offers import enums
from my_offers.repositories.monolith_cian_announcementapi.entities import PublishTerm, PublishTerms
from my_offers.repositories.monolith_cian_announcementapi.entities.publish_term import Services
from my_offers.services.announcement.fields.services import get_services


@pytest.mark.parametrize(
    ('publish_terms', 'expected'),
    (
        (None, []),
        (PublishTerms(), []),
        (PublishTerms(terms=[PublishTerm()]), []),
        (PublishTerms(terms=[PublishTerm(services=[Services.highlight])]), []),
        (
            PublishTerms(
                terms=[
                    PublishTerm(services=[Services.highlight]),
                    PublishTerm(services=[Services.paid]),
                ]
            ),
            [enums.OfferServices.paid],
        ),
    )
)
def test_get_services(mocker, publish_terms, expected):
    # arrange & act
    result = get_services(publish_terms)

    # assert
    assert result == expected
