import pytest

from my_offers.services.offers.helpers.search_text import prepare_search_text


@pytest.mark.parametrize(
    ('search_text', 'expected'),
    (
        ('+7 926 390 9970 8 (926) 3909071 926-490-90-70', ' 9263909970 9263909071 9264909070'),
        ('+7 926 390 9970 Москва д156', ' 9263909970 Москва д156'),
        ('Москва д156', 'Москва д156'),
    )
)
def test_prepare_search_text(search_text, expected):
    # arrange & act
    result = prepare_search_text(search_text)

    # assert
    assert result == expected
