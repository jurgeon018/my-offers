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
            '165456885 9994606004 9982276978 Россия, Ростов-на-Дону, Большая Садовая '
            'улица, 73 Ростовская область Ростов-на-Дону Большая Садовая улица 73 д73 д '
            '73 73д Кировский Центр район 1-комн.\xa0кв., 123\xa0м², 1/3\xa0этаж zzzzzzzzz 1 комн '
            'комнатная 1 3 выапывапвыапыпыпвыапывапывапыап'
        ),
        (
            object_model_mapper.map_from(load_json_data(__file__, 'announcement_moscow.json')),
            '138496 Россия, Москва, Братиславская улица Москва Братиславская улица '
            'Братиславская метро 3-комн.\xa0кв., 90\xa0м², 22/22\xa0этаж 3 комн комнатная 22 22 '
            'Офисно  деловой центр с торговыми помещениями и апартаментами,         '
            '2-сан.узла. подземный паркинг 900000р. машиноместо.'
        ),
        (
            object_model_mapper.map_from(load_json_data(__file__, 'announcement_jk.json')),
            '227177044 4991165117 Россия, Москва, Михневская улица, 8 Москва Михневская '
            'улица 8 д8 д 8 8д Царицыно метро ЮАО Бирюлево Восточное район '
            'Бирюлёво-Пассажирская Бирюлёво-Пассажирская Булатниково Булатниково '
            'Бирюлёво-Товарная Бирюлёво-Товарная станиция Загорье ЖК жилой комплекс '
            '3-комн.\xa0кв., 110\xa0м², 9/15\xa0этаж Просторная трёшка в ЖК "Загорье"! 3 комн '
            'комнатная 9 15 Продается просторная 3х-комнатная квартира 2483 площадью '
            '110,0 кв.м. в ЖК Загорье на 9 этаже 15 этажного дома.'
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
def test__get_house(house, expected):
    # arrange & act
    result = _get_house([AddressInfo(name=house, type=Type.house)])

    # assert
    assert result == expected


def test__get_house__not_adrress__empty():
    # arrange & act
    result = _get_house(None)

    # assert
    assert result == []


def test__get_house__wrong_format__empty():
    # arrange & act
    result = _get_house([AddressInfo(name='ZZZ', type=Type.house)])

    # assert
    assert result == []
