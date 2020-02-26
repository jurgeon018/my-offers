import pytest

from my_offers.services.announcement.fields.prices import get_prices


@pytest.mark.parametrize(
    ('bargain_terms', 'total_area', 'expected'),
    (
        (
            {
                'price': 11111.0,
                'vatType': 'usn',
                'agentFee': 0,
                'currency': 'rur',
                'clientFee': 0,
                'leaseType': 'direct',
                'priceType': 'sotka',
                'vatIncluded': True,
                'prepayMonths': 3,
                'leaseTermType': 'longTerm',
                'paymentPeriod': 'monthly',
                'includedOptions': [],
            },
            None,
            (None, 111.11),
        ),
        (
            {
                'price': 11111.0,
                'vatType': 'usn',
                'agentFee': 0,
                'currency': 'rur',
                'clientFee': 0,
                'leaseType': 'direct',
                'priceType': 'all',
                'vatIncluded': True,
                'prepayMonths': 3,
                'leaseTermType': 'longTerm',
                'paymentPeriod': 'monthly',
                'includedOptions': [],
            },
            None,
            (11111.0, None),
        ),
        (
            {
                'price': 11111.0,
                'vatType': 'usn',
                'agentFee': 0,
                'currency': 'rur',
                'clientFee': 0,
                'leaseType': 'direct',
                'priceType': 'sotka',
                'vatIncluded': True,
                'prepayMonths': 3,
                'leaseTermType': 'longTerm',
                'paymentPeriod': 'monthly',
                'includedOptions': [],
            },
            7,
            (777.77, 111.11),
        ),
        (
            {
                'price': 9070000.0,
                'currency': 'rur',
                'priceType': 'all',
                'includedOptions': []
            },
            90.7,
            (9070000.0, 100000.0),
        ),
        (
            {
                'price': 50000.0,
                'vatType': 'usn',
                'agentFee': 5,
                'currency': 'rur',
                'clientFee': 0,
                'leaseType': 'direct',
                'priceType': 'hectare',
                'vatIncluded': True,
                'minLeaseTerm': 6,
                'prepayMonths': 1,
                'leaseTermType': 'longTerm',
                'paymentPeriod': 'monthly',
                'hasGracePeriod': True,
                'includedOptions': [],
                'securityDeposit': 20000,
            },
            345,
            (1725.0, 5.0),
        ),
        (
            {
                'price': 360000.0,
                'deposit': 200000,
                'vatType': 'included',
                'agentFee': 70,
                'currency': 'rur',
                'vatPrice': 60000.0,
                'clientFee': 70,
                'priceType': 'squareMeter',
                'vatIncluded': True,
                'prepayMonths': 2,
                'leaseTermType': 'longTerm',
                'paymentPeriod': 'monthly',
                'bargainAllowed': False,
                'utilitiesTerms': {
                    'price': 0.0,
                    'includedInPrice': True
                },
                'includedOptions': []
            },
            20,
            (7200000.0, 360000.0),
        ),
        (
            {'currency': 'rur'},
            90.7,
            (None, None),
        ),
    ),
)
def test__get_prices(bargain_terms, total_area, expected):
    # arrange & act
    result = get_prices(bargain_terms=bargain_terms, total_area=total_area)

    # assert
    assert result == expected
