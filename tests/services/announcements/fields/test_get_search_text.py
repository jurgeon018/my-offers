import pytest

from my_offers.mappers.object_model import object_model_mapper
from my_offers.services.announcement.fields.search_text import get_search_text
from tests.utils import load_json_data


@pytest.mark.parametrize(
    ('announcement', 'expected'),
    (
        (
            object_model_mapper.map_from(load_json_data(__file__, 'announcement.json')),
            '165456885 zzzzzzzzz выапывапвыапыпыпвыапывапывапыап +79994606004 +79982276978 Россия, '
            'Ростов-на-Дону, Большая Садовая улица, 73'
        ),
        (
            object_model_mapper.map_from(load_json_data(__file__, 'announcement_moscow.json')),
            '138496 Офисно  деловой центр с торговыми помещениями и '
            'апартаментами,         2-сан.узла. '
            'подземный паркинг 900000р. машиноместо. Россия, Москва, Братиславская улица '
            'Братиславская'
        ),
    )
)
def test__get_search_text(announcement, expected):
    # arrange & act
    result = get_search_text(announcement)

    # assert
    assert result == expected
