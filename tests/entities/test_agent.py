import pytest

from my_offers.entities import AgentName


@pytest.mark.parametrize(
    ('first_name', 'last_name', 'middle_name', 'expected'),
    (
        (None, None, None, None),
        (None, None, 'Zz', None),
        ('Yy', None, 'Zz', 'Yy'),
        (None, 'Xx', 'Zz', 'Xx'),
        ('Yy', 'Xx', 'Zz', 'Yy Xx'),
        ('Yy', 'Xx', None, 'Yy Xx'),
    )
)
def test_agent_get_name(mocker, first_name, last_name, middle_name, expected):
    # arrange
    agent = AgentName(id=1, first_name=first_name, last_name=last_name, middle_name=middle_name)

    # act
    result = agent.get_name()

    # assert
    assert result == expected
