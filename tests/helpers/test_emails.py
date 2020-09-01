import pytest

from my_offers.helpers.emails import is_correct_email


@pytest.mark.parametrize('email', [
    'a@a.com',
    'a.asdas@a.com',
    'A@A.COM',
])
def test__validate_email__valid_email(email):
    # act, assert
    assert is_correct_email(email) is True


@pytest.mark.parametrize('email', [
    'aaaa',
    'aaaa@asd',
    'aaaa.com',
    'тест@тест.ком',
])
def test__validate_email__invalid_email(email):
    # act, assert
    assert is_correct_email(email) is False
