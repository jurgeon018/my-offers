import pytest

from my_offers.mappers.object_model import object_model_mapper
from my_offers.repositories.monolith_cian_announcementapi.entities import AddressInfo
from my_offers.repositories.monolith_cian_announcementapi.entities.address_info import Type
from my_offers.services.announcement.fields.search_text import _get_house, get_search_text
from tests.utils import load_json_data


@pytest.mark.parametrize(
    ('announcement', 'expected'),
    (
        (
            object_model_mapper.map_from(load_json_data(__file__, 'announcement.json')),
            '165456885 +79994606004 +79982276978 Россия, Ростов-на-Дону, Большая Садовая улица, 73 Ростовская '
            'Ростов-на-Дону Большая Садовая 73 д73 д 73 73д Кировский Центр 1-комн. кв., 123 м², '
            '1/3 этаж zzzzzzzzz 1 3 выапывапвыапыпыпвыапывапывапыап'
        ),
        (
            object_model_mapper.map_from(load_json_data(__file__, 'announcement_moscow.json')),
            '138496 Россия, Москва, Братиславская улица Москва Братиславская Братиславская 3-комн. кв., 90 м², '
            '22/22 этаж 22 22 Офисно  деловой центр с торговыми помещениями и апартаментами,         '
            '2-сан.узла. подземный паркинг 900000р. машиноместо.'
        ),
    )
)
def test__get_search_text(announcement, expected):
    # arrange & act
    result = get_search_text(announcement)

    # assert
    assert result == expected


@pytest.mark.parametrize(
    ('house', 'expected'),
    (
        ('17/3к2бс5а', ['д17/3', 'д', '17/3', '17/3д', 'к2б', 'к', '2б', '2бк', 'с5а', 'с', '5а', '5ас']),
        ('вл56Б', ['вл56Б', 'вл', '56Б', '56Бвл']),
        ('17', ['д17', 'д', '17', '17д']),
        ('17к12', ['д17', 'д', '17', '17д', 'к12', 'к', '12', '12к']),
    )
)
def test___get_house(house, expected):
    # arrange & act
    result = _get_house([AddressInfo(name=house, type=Type.house)])

    # assert
    assert result == expected
