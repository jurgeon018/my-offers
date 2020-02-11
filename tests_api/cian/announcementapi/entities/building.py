# pylint: skip-file
"""

Code generated by new-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client announcementapi`

new-codegen version: 4.0.0

"""
from dataclasses import dataclass
from typing import List, Optional

from cian_enum import NoFormat, StrEnum

from .commercial_building_infrastructure import CommercialBuildingInfrastructure
from .cranage_type import CranageType
from .deadline import Deadline
from .lift_type import LiftType
from .opening_hours import OpeningHours
from .parking import Parking


class AccessType(StrEnum):
    __value_format__ = NoFormat
    free = 'free'
    """Свободный"""
    pass_system = 'passSystem'
    """Пропускная система"""


class ClassType(StrEnum):
    __value_format__ = NoFormat
    a = 'a'
    """A"""
    a_plus = 'aPlus'
    """A+"""
    b = 'b'
    """B"""
    b_minus = 'bMinus'
    """B-"""
    b_plus = 'bPlus'
    """B+"""
    c = 'c'
    """C"""
    c_plus = 'cPlus'
    """C+"""
    d = 'd'
    """D"""


class ConditionRatingType(StrEnum):
    __value_format__ = NoFormat
    excellent = 'excellent'
    """Отличное"""
    good = 'good'
    """Хорошее"""
    satisfactory = 'satisfactory'
    """Удовлетворительное"""


class ConditioningType(StrEnum):
    __value_format__ = NoFormat
    central = 'central'
    """Центральное"""
    local = 'local'
    """Местное"""
    no = 'no'
    """Нет"""


class ExtinguishingSystemType(StrEnum):
    __value_format__ = NoFormat
    alarm = 'alarm'
    """Сигнализация"""
    gas = 'gas'
    """Газовая"""
    hydrant = 'hydrant'
    """Гидрантная"""
    no = 'no'
    """Нет"""
    powder = 'powder'
    """Порошковая"""
    sprinkler = 'sprinkler'
    """Спринклерная"""


class ExtinguishingSystemTypes(StrEnum):
    __value_format__ = NoFormat
    alarm = 'alarm'
    gas = 'gas'
    hydrant = 'hydrant'
    no = 'no'
    powder = 'powder'
    sprinkler = 'sprinkler'


class GatesType(StrEnum):
    __value_format__ = NoFormat
    at_zero = 'atZero'
    """На нулевой отметке"""
    dock_type = 'dockType'
    """Докового типа"""
    on_ramp = 'onRamp'
    """На пандусе"""


class HeatingType(StrEnum):
    __value_format__ = NoFormat
    autonomous = 'autonomous'
    """Автономное"""
    boiler = 'boiler'
    """Котел"""
    central = 'central'
    """Центральное"""
    fireplace = 'fireplace'
    """Камин"""
    no = 'no'
    """Нет"""
    other = 'other'
    """Другое"""
    stove = 'stove'
    """Печь"""
    central_gas = 'centralGas'
    """центральное газовое"""
    central_coal = 'centralCoal'
    """центральное угольное"""
    electric = 'electric'
    """Электрическое"""
    autonomous_gas = 'autonomousGas'
    """Автономное газовое"""
    diesel = 'diesel'
    """Дизельное"""
    solid_fuel_boiler = 'solidFuelBoiler'
    """Твердотопливный котел"""


class HouseLineType(StrEnum):
    __value_format__ = NoFormat
    first = 'first'
    """Первая"""
    other = 'other'
    """Иная"""
    second = 'second'
    """Вторая"""


class MaterialType(StrEnum):
    __value_format__ = NoFormat
    block = 'block'
    """Блочный"""
    boards = 'boards'
    """Щитовой"""
    brick = 'brick'
    """Кирпичный"""
    monolith = 'monolith'
    """Монолитный"""
    monolith_brick = 'monolithBrick'
    """Монолитно-кирпичный"""
    old = 'old'
    """Старый фонд"""
    panel = 'panel'
    """Панельный"""
    stalin = 'stalin'
    """Сталинский"""
    wood = 'wood'
    """Деревянный"""
    wireframe = 'wireframe'
    """Каркасный"""
    aerocrete_block = 'aerocreteBlock'
    """Газобетонный блок"""
    gas_silicate_block = 'gasSilicateBlock'
    """Газосиликатный блок"""
    foam_concrete_block = 'foamConcreteBlock'
    """Пенобетонный блок"""


class ShoppingCenterScaleType(StrEnum):
    __value_format__ = NoFormat
    district = 'district'
    """Районный"""
    microdistrict = 'microdistrict'
    """Микрорайонный"""
    okrug = 'okrug'
    """Окружной"""
    regional = 'regional'
    """Региональный"""
    super_okrug = 'superOkrug'
    """Суперокружной"""
    super_regional = 'superRegional'
    """Суперрегиональный"""


class StatusType(StrEnum):
    __value_format__ = NoFormat
    new_building = 'newBuilding'
    """Новостройка/Строящееся"""
    operational = 'operational'
    """Действующее"""
    project = 'project'
    """Проект"""
    secondary = 'secondary'
    """Вторичный рынок"""
    under_construction = 'underConstruction'
    """Строящееся"""


class Type(StrEnum):
    __value_format__ = NoFormat
    administrative_building = 'administrativeBuilding'
    """Административное здание"""
    business_center = 'businessCenter'
    """Бизнес-центр"""
    business_center2 = 'businessCenter2'
    """Деловой центр"""
    business_park = 'businessPark'
    """Бизнес-парк"""
    business_quarter = 'businessQuarter'
    """Бизнес-квартал"""
    free = 'free'
    """Объект свободного назначения"""
    industrial_complex = 'industrialComplex'
    """Производственный комплекс"""
    industrial_park = 'industrialPark'
    """Индустриальный парк"""
    industrial_site = 'industrialSite'
    """Промплощадка"""
    industrial_warehouse_complex = 'industrialWarehouseComplex'
    """Производственно-складской комплекс"""
    logistics_center = 'logisticsCenter'
    """Логистический центр"""
    logistics_complex = 'logisticsComplex'
    """Логистический комплекс"""
    mansion = 'mansion'
    """Особняк"""
    manufacture_building = 'manufactureBuilding'
    """Производственное здание"""
    manufacturing_facility = 'manufacturingFacility'
    """Производственный цех"""
    modular = 'modular'
    """Модульное здание"""
    multifunctional_complex = 'multifunctionalComplex'
    """Многофункциональный комплекс"""
    office_and_hotel_complex = 'officeAndHotelComplex'
    """Офисно-гостиничный комплекс"""
    office_and_residential_complex = 'officeAndResidentialComplex'
    """Офисно-жилой комплекс"""
    office_and_warehouse = 'officeAndWarehouse'
    """Офисно-складское здание"""
    office_and_warehouse_complex = 'officeAndWarehouseComplex'
    """Офисно-складской комплекс"""
    office_building = 'officeBuilding'
    """Офисное здание"""
    office_industrial_complex = 'officeIndustrialComplex'
    """Офисно-производственный комплекс"""
    old = 'old'
    """Старый фонд"""
    other = 'other'
    """Другое"""
    outlet = 'outlet'
    """Аутлет"""
    property_complex = 'propertyComplex'
    """Имущественный комплекс"""
    residential_complex = 'residentialComplex'
    """Жилой комплекс"""
    residential_fund = 'residentialFund'
    """Жилой фонд"""
    residential_house = 'residentialHouse'
    """Жилой дом"""
    shopping_and_business_complex = 'shoppingAndBusinessComplex'
    """Торгово-деловой комплекс"""
    shopping_and_community_center = 'shoppingAndCommunityCenter'
    """Торгово-общественный центр"""
    shopping_and_entertainment_center = 'shoppingAndEntertainmentCenter'
    """Торгово-развлекательный центр"""
    shopping_center = 'shoppingCenter'
    """Торговый центр"""
    specialized_shopping_center = 'specializedShoppingCenter'
    """Специализированный торговый центр"""
    standalone_building = 'standaloneBuilding'
    """Отдельно стоящее здание"""
    technopark = 'technopark'
    """Технопарк"""
    trading_office_complex = 'tradingOfficeComplex'
    """Торгово-офисный комплекс"""
    uninhabited_fund = 'uninhabitedFund'
    """Нежилой фонд"""
    warehouse = 'warehouse'
    """Склад"""
    warehouse_complex = 'warehouseComplex'
    """Складской комплекс"""
    office_quarter = 'officeQuarter'
    """Офисный квартал"""
    office_center = 'officeCenter'
    """Офисный центр"""
    business_quarter2 = 'businessQuarter2'
    """Деловой квартал"""
    business_house = 'businessHouse'
    """Деловой дом"""
    trading_house = 'tradingHouse'
    """Торговый дом"""
    office_complex = 'officeComplex'
    """Офисный комплекс"""
    trade_and_exhibition_complex = 'tradeAndExhibitionComplex'
    """Торгово-выставочный комплекс"""
    shopping_complex = 'shoppingComplex'
    """Торговый комплекс"""
    shopping_and_warehouse_complex = 'shoppingAndWarehouseComplex'
    """Торгово-складской комплекс"""
    logistics_park = 'logisticsPark'
    """Логистический парк"""


class VentilationType(StrEnum):
    __value_format__ = NoFormat
    forced = 'forced'
    """Приточная"""
    natural = 'natural'
    """Естественная"""
    no = 'no'
    """Нет"""


class WorkingDaysType(StrEnum):
    __value_format__ = NoFormat
    everyday = 'everyday'
    """Ежедневно"""
    weekdays = 'weekdays'
    """Будни"""
    weekends = 'weekends'
    """Выходные"""


@dataclass
class Building:
    """Здание"""

    accessType: Optional[AccessType] = None
    """Вход"""
    buildYear: Optional[int] = None
    """Год постройки"""
    cargoLiftsCount: Optional[int] = None
    """Количество грузовых лифтов"""
    ceilingHeight: Optional[float] = None
    """Высота потолков, м"""
    classType: Optional[ClassType] = None
    """Класс"""
    columnGrid: Optional[str] = None
    """Сетка колонн"""
    conditionRatingType: Optional[ConditionRatingType] = None
    """Состояние"""
    conditioningType: Optional[ConditioningType] = None
    """Кондиционирование"""
    cranageTypes: Optional[List[CranageType]] = None
    """Крановое оборудование"""
    deadline: Optional[Deadline] = None
    """Срок сдачи"""
    developer: Optional[str] = None
    """Застройщик"""
    extinguishingSystemType: Optional[ExtinguishingSystemType] = None
    """Система пожаротушения"""
    extinguishingSystemTypes: Optional[List[ExtinguishingSystemTypes]] = None
    """Системы пожаротушения"""
    floorsCount: Optional[int] = None
    """Количество этажей в здании"""
    gatesType: Optional[GatesType] = None
    """Тип ворот"""
    hasGarbageChute: Optional[bool] = None
    """Мусоропровод"""
    heatingType: Optional[HeatingType] = None
    """Отопление"""
    houseLineType: Optional[HouseLineType] = None
    """Линия домов"""
    infrastructure: Optional[CommercialBuildingInfrastructure] = None
    """Инфраструктура"""
    liftTypes: Optional[List[LiftType]] = None
    """Лифт"""
    managementCompany: Optional[str] = None
    """Управляющая компания"""
    materialType: Optional[MaterialType] = None
    """Тип дома"""
    name: Optional[str] = None
    """Название"""
    openingHours: Optional[OpeningHours] = None
    """Часы работы"""
    parking: Optional[Parking] = None
    """Парковка"""
    passengerLiftsCount: Optional[int] = None
    """Количество пассажирских лифтов"""
    series: Optional[str] = None
    """Серия дома"""
    shoppingCenterScaleType: Optional[ShoppingCenterScaleType] = None
    """Масштаб торгового центра"""
    statusType: Optional[StatusType] = None
    """Категория"""
    tenants: Optional[str] = None
    """Арендаторы"""
    totalArea: Optional[float] = None
    """Общая площадь, м²"""
    type: Optional[Type] = None
    """Тип"""
    ventilationType: Optional[VentilationType] = None
    """Вентиляция"""
    workingDaysType: Optional[WorkingDaysType] = None
    """Рабочие дни"""
