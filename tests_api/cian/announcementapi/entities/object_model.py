# pylint: skip-file
"""

Code generated by new-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client announcementapi`

new-codegen version: 4.0.1

"""
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from cian_enum import NoFormat, StrEnum

from .auction import Auction
from .bargain_terms import BargainTerms
from .building import Building
from .business_shopping_center import BusinessShoppingCenter
from .commercial_specialty import CommercialSpecialty
from .cpl_moderation import CplModeration
from .drainage import Drainage
from .electricity import Electricity
from .flags import Flags
from .garage import Garage
from .gas import Gas
from .geo import Geo
from .home_owner import HomeOwner
from .kp import Kp
from .land import Land
from .monthly_income import MonthlyIncome
from .phone import Phone
from .photo import Photo
from .platform import Platform
from .publish_terms import PublishTerms
from .rent_by_parts import RentByParts
from .video import Video
from .water import Water


class AccessType(StrEnum):
    __value_format__ = NoFormat
    free = 'free'
    """Свободный"""
    pass_system = 'passSystem'
    """Пропускная система"""


class CallTrackingProvider(StrEnum):
    __value_format__ = NoFormat
    beeline = 'beeline'
    mtt = 'MTT'
    mts = 'mts'
    qa = 'qa'


class Category(StrEnum):
    __value_format__ = NoFormat
    bed_rent = 'bedRent'
    """Койко-место"""
    building_rent = 'buildingRent'
    """Здание"""
    building_sale = 'buildingSale'
    """Здание"""
    business_rent = 'businessRent'
    """Готовый бизнес"""
    business_sale = 'businessSale'
    """Готовый бизнес"""
    car_service_rent = 'carServiceRent'
    """Аренда автосервис"""
    car_service_sale = 'carServiceSale'
    """Продажа автосервиса"""
    commercial_land_rent = 'commercialLandRent'
    """Коммерческая земля"""
    commercial_land_sale = 'commercialLandSale'
    """Коммерческая земля"""
    cottage_rent = 'cottageRent'
    """Коттедж"""
    cottage_sale = 'cottageSale'
    """Коттедж"""
    daily_bed_rent = 'dailyBedRent'
    """Посуточная аренда койко-места"""
    daily_flat_rent = 'dailyFlatRent'
    """Посуточная аренда квартиры"""
    daily_house_rent = 'dailyHouseRent'
    """Посуточная аренда дома, дачи, коттеджа"""
    daily_room_rent = 'dailyRoomRent'
    """Посуточная аренда комнаты"""
    domestic_services_rent = 'domesticServicesRent'
    """Аренда помещения под бытовые услуги"""
    domestic_services_sale = 'domesticServicesSale'
    """Продажа помещения под бытовые услуги"""
    flat_rent = 'flatRent'
    """Квартира"""
    flat_sale = 'flatSale'
    """Квартира"""
    flat_share_sale = 'flatShareSale'
    """Доля в квартире"""
    free_appointment_object_rent = 'freeAppointmentObjectRent'
    """Помещение свободного назначения"""
    free_appointment_object_sale = 'freeAppointmentObjectSale'
    """Помещение свободного назначения"""
    garage_rent = 'garageRent'
    """Гараж"""
    garage_sale = 'garageSale'
    """Гараж"""
    house_rent = 'houseRent'
    """Дом/дача"""
    house_sale = 'houseSale'
    """Дом/дача"""
    house_share_rent = 'houseShareRent'
    """Часть дома"""
    house_share_sale = 'houseShareSale'
    """Часть дома"""
    industry_rent = 'industryRent'
    """Производство"""
    industry_sale = 'industrySale'
    """Производство"""
    land_sale = 'landSale'
    """Участок"""
    new_building_flat_sale = 'newBuildingFlatSale'
    """Квартира в новостройке"""
    office_rent = 'officeRent'
    """Офис"""
    office_sale = 'officeSale'
    """Офис"""
    public_catering_rent = 'publicCateringRent'
    """Аренда общепита"""
    public_catering_sale = 'publicCateringSale'
    """Продажа общепита"""
    room_rent = 'roomRent'
    """Комната"""
    room_sale = 'roomSale'
    """Комната"""
    shopping_area_rent = 'shoppingAreaRent'
    """Торговая площадь"""
    shopping_area_sale = 'shoppingAreaSale'
    """Торговая площадь"""
    townhouse_rent = 'townhouseRent'
    """Таунхаус"""
    townhouse_sale = 'townhouseSale'
    """Таунхаус"""
    warehouse_rent = 'warehouseRent'
    """Склад"""
    warehouse_sale = 'warehouseSale'
    """Склад"""


class ConditionRatingType(StrEnum):
    __value_format__ = NoFormat
    excellent = 'excellent'
    """Отличное"""
    good = 'good'
    """Хорошее"""
    satisfactory = 'satisfactory'
    """Удовлетворительное"""


class ConditionType(StrEnum):
    __value_format__ = NoFormat
    cosmetic_repairs_required = 'cosmeticRepairsRequired'
    """Требуется косметический ремонт"""
    design = 'design'
    """Дизайнерский ремонт"""
    finishing = 'finishing'
    """Под чистовую отделку"""
    major_repairs_required = 'majorRepairsRequired'
    """Требуется капитальный ремонт"""
    office = 'office'
    """Офисная отделка"""
    typical = 'typical'
    """Типовой ремонт"""


class Decoration(StrEnum):
    __value_format__ = NoFormat
    fine = 'fine'
    """Чистовая"""
    rough = 'rough'
    """Черновая"""
    without = 'without'
    """Без отделки"""


class DrainageType(StrEnum):
    __value_format__ = NoFormat
    central = 'central'
    """Центральная"""
    septic_tank = 'septicTank'
    """Септик"""
    storm = 'storm'
    """Ливневая"""
    treatment_facilities = 'treatmentFacilities'
    """Очистные сооружения"""


class DrivewayType(StrEnum):
    __value_format__ = NoFormat
    no = 'no'
    """Нет"""
    asphalt = 'asphalt'
    """Асфальтированная дорога"""
    ground = 'ground'
    """Грунтовая дорога"""


class ElectricityType(StrEnum):
    __value_format__ = NoFormat
    border = 'border'
    """По границе участка"""
    main = 'main'
    """Магистральное"""
    transformer_vault = 'transformerVault'
    """Трансформаторная будка"""


class EstateType(StrEnum):
    __value_format__ = NoFormat
    owned = 'owned'
    """В собственности"""
    rent = 'rent'
    """В аренде"""


class FlatType(StrEnum):
    __value_format__ = NoFormat
    open_plan = 'openPlan'
    """Свободная планировка"""
    rooms = 'rooms'
    """Комнаты"""
    studio = 'studio'
    """Студия"""


class FloorMaterialType(StrEnum):
    __value_format__ = NoFormat
    polymeric = 'polymeric'
    """Полимерный"""
    concrete = 'concrete'
    """Бетон"""
    linoleum = 'linoleum'
    """Линолеум"""
    asphalt = 'asphalt'
    """Асфальт"""
    tile = 'tile'
    """Плитка"""
    self_leveling = 'selfLeveling'
    """Наливной"""
    reinforced_concrete = 'reinforcedConcrete'
    """Железобетон"""
    wood = 'wood'
    """Деревянный"""
    laminate = 'laminate'
    """Ламинат"""


class FurniturePresence(StrEnum):
    __value_format__ = NoFormat
    no = 'no'
    """Нет"""
    optional = 'optional'
    """По желанию"""
    yes = 'yes'
    """Есть"""


class GasType(StrEnum):
    __value_format__ = NoFormat
    border = 'border'
    """По границе участка"""
    main = 'main'
    """Магистральное"""


class InputType(StrEnum):
    __value_format__ = NoFormat
    common_from_street = 'commonFromStreet'
    """Общий с улицы"""
    common_from_yard = 'commonFromYard'
    """Общий со двора"""
    separate_from_street = 'separateFromStreet'
    """Отдельный с улицы"""
    separate_from_yard = 'separateFromYard'
    """Отдельный со двора"""


class Layout(StrEnum):
    __value_format__ = NoFormat
    cabinet = 'cabinet'
    """Кабинетная"""
    mixed = 'mixed'
    """Смешанная"""
    open_space = 'openSpace'
    """Открытая"""
    corridorplan = 'corridorplan'
    """Коридорная"""


class PermittedUseType(StrEnum):
    __value_format__ = NoFormat
    agricultural = 'agricultural'
    """Cельскохозяйственное использование"""
    individual_housing_construction = 'individualHousingConstruction'
    """Индивидуальное жилищное строительство (ИЖС)"""
    lowrise_housing = 'lowriseHousing'
    """Малоэтажное жилищное строительство (МЖС)"""
    highrise_buildings = 'highriseBuildings'
    """Высотная застройка"""
    public_use_of_capital_construction = 'publicUseOfCapitalConstruction'
    """Общественное использование объектов капитального строительства"""
    business_management = 'businessManagement'
    """Деловое управление"""
    shopping_centers = 'shoppingCenters'
    """Торговые центры"""
    hotel_amenities = 'hotelAmenities'
    """Гостиничное обслуживание"""
    service_vehicles = 'serviceVehicles'
    """Обслуживание автотранспорта"""
    leisure = 'leisure'
    """Отдых (рекреация)"""
    industry = 'industry'
    """Промышленность"""
    warehouses = 'warehouses'
    """Склады"""
    common_use_area = 'commonUseArea'
    """Общее пользование территории"""


class PlacementType(StrEnum):
    __value_format__ = NoFormat
    shopping_mall = 'shoppingMall'
    """Помещение в торговом комплексе"""
    street_retail = 'streetRetail'
    """Street retail"""


class PropertyType(StrEnum):
    __value_format__ = NoFormat
    building = 'building'
    """здание"""
    free_appointment = 'freeAppointment'
    """помещение свободного назначения"""
    garage = 'garage'
    """гараж"""
    industry = 'industry'
    """производство"""
    land = 'land'
    """земля"""
    office = 'office'
    """офис"""
    shopping_area = 'shoppingArea'
    """торговая площадь"""
    warehouse = 'warehouse'
    """склад"""


class RepairType(StrEnum):
    __value_format__ = NoFormat
    cosmetic = 'cosmetic'
    """Косметический"""
    design = 'design'
    """Дизайнерский"""
    euro = 'euro'
    """Евроремонт"""
    no = 'no'
    """Без ремонта"""


class RoomType(StrEnum):
    __value_format__ = NoFormat
    both = 'both'
    """Оба варианта"""
    combined = 'combined'
    """Совмещенная"""
    separate = 'separate'
    """Изолированная"""


class Source(StrEnum):
    __value_format__ = NoFormat
    website = 'website'
    """Ручная подача"""
    upload = 'upload'
    """Выгрузки"""
    mobile_app = 'mobileApp'
    """Мобильное приложение"""


class Status(StrEnum):
    __value_format__ = NoFormat
    draft = 'Draft'
    """11 - Черновик"""
    published = 'Published'
    """12 - Опубликовано"""
    deactivated = 'Deactivated'
    """14 - Деактивировано (ранее было скрыто Hidden)"""
    refused = 'Refused'
    """15 - Отклонено модератором"""
    deleted = 'Deleted'
    """16 - Удалён"""
    sold = 'Sold'
    """17 - Продано/Сдано"""
    moderate = 'Moderate'
    '18 - Требует модерации\r\nДанный статус исчез - оставим для совместимости'
    removed_by_moderator = 'RemovedByModerator'
    """19 - Удалено модератором"""
    blocked = 'Blocked'
    """20 - объявление снято с публикации по причине применения санкции "приостановки публикации\""""


class WaterType(StrEnum):
    __value_format__ = NoFormat
    central = 'central'
    """Центральное"""
    pumping_station = 'pumpingStation'
    """Водонапорная станция"""
    water_intake_facility = 'waterIntakeFacility'
    """Водозаборный узел"""
    water_tower = 'waterTower'
    """Водонапорная башня"""


class WcLocationType(StrEnum):
    __value_format__ = NoFormat
    indoors = 'indoors'
    """В доме"""
    outdoors = 'outdoors'
    """На улице"""


class WcType(StrEnum):
    __value_format__ = NoFormat
    combined = 'combined'
    """Совмещенный"""
    separate = 'separate'
    """Раздельный"""


class WindowsViewType(StrEnum):
    __value_format__ = NoFormat
    street = 'street'
    """На улицу"""
    yard = 'yard'
    """Во двор"""
    yard_and_street = 'yardAndStreet'
    """На улицу и двор"""


@dataclass
class ObjectModel:
    """Модель объявления."""

    bargainTerms: BargainTerms
    """Условия сделки"""
    category: Category
    """Категория объявления"""
    phones: List[Phone]
    """Телефон"""
    accessType: Optional[AccessType] = None
    """Доступ"""
    additionalPhoneLinesAllowed: Optional[bool] = None
    """Доп. линии"""
    allRoomsArea: Optional[str] = None
    'Площадь комнат, м².\r\n+ для обозначения смежных комнат, - для раздельных комнат.\r\n            \r\nПоле RoomDefinitions имеет приоритет - если оно задано, поле AllRoomsArea будет переопределено.'
    archivedDate: Optional[datetime] = None
    """Дата переноса объявления в архив."""
    areaParts: Optional[List[RentByParts]] = None
    """Сдача частей в аренду"""
    auction: Optional[Auction] = None
    availableFrom: Optional[str] = None
    """Дата освобождения"""
    balconiesCount: Optional[int] = None
    """Количество балконов"""
    bedroomsCount: Optional[int] = None
    """Количество спален"""
    bedsCount: Optional[int] = None
    """Количество спальных мест"""
    building: Optional[Building] = None
    """Информация о здании"""
    businessShoppingCenter: Optional[BusinessShoppingCenter] = None
    """ТЦ/БЦ, <a href="https://www.cian.ru/cian-api/site/v1/business-shopping-centers-export/to-client-excel/">Скачать список ID</a>"""
    cadastralNumber: Optional[str] = None
    """Кадастровый номер"""
    callTrackingProvider: Optional[CallTrackingProvider] = None
    """Тип подключенного calltracking'а"""
    canParts: Optional[bool] = None
    """Можно частями"""
    childrenAllowed: Optional[bool] = None
    """Можно с детьми"""
    cianId: Optional[int] = None
    """ID объявления на ЦИАНе"""
    cianUserId: Optional[int] = None
    """ID пользователя в ЦИАНе"""
    combinedWcsCount: Optional[int] = None
    """Количество совместных санузлов"""
    conditionRatingType: Optional[ConditionRatingType] = None
    """Состояние"""
    conditionType: Optional[ConditionType] = None
    """Состояние"""
    cplModeration: Optional[CplModeration] = None
    'Данные для CPL модерации.<br />\r\nЗаполняются данными дольщика из ДДУ<br />\r\nДля физ. лица необходимо указать ФИО, для юр. лица ИНН.<br />\r\nПоля являются обязательными в следующих регионах: Москва, Московская область, Санкт-Петербург, Ленинградская область.'
    creationDate: Optional[datetime] = None
    """Дата создания объявления"""
    decoration: Optional[Decoration] = None
    """Отделка"""
    description: Optional[str] = None
    """Текст объявления"""
    drainage: Optional[Drainage] = None
    """Канализация"""
    drainageCapacity: Optional[int] = None
    """Объем, м³/сутки"""
    drainageType: Optional[DrainageType] = None
    """Тип канализации"""
    drivewayType: Optional[DrivewayType] = None
    """Подъездные пути"""
    editDate: Optional[datetime] = None
    """Дата редактирования объявления."""
    electricity: Optional[Electricity] = None
    """Электроснабжение"""
    electricityPower: Optional[int] = None
    """Мощность, кВТ"""
    electricityType: Optional[ElectricityType] = None
    """Тип электроснабжения"""
    emlsId: Optional[str] = None
    """Emls Id объявления"""
    estateType: Optional[EstateType] = None
    """Недвижимость"""
    feedboxMultiOfferKey: Optional[str] = None
    """Ключ мультиобъявления из Feedbox."""
    flags: Optional[Flags] = None
    """Флаги объявления."""
    flatType: Optional[FlatType] = None
    """Тип квартиры"""
    floorMaterialType: Optional[FloorMaterialType] = None
    """Материал пола"""
    floorNumber: Optional[int] = None
    """Этаж"""
    furniturePresence: Optional[FurniturePresence] = None
    """Мебель"""
    garage: Optional[Garage] = None
    """Тип гаража"""
    gas: Optional[Gas] = None
    """Газоснабжение"""
    gasCapacity: Optional[int] = None
    """Емкость, м³/час"""
    gasPressure: Optional[int] = None
    """Давление, Мпа"""
    gasType: Optional[GasType] = None
    """Тип газоснабжения"""
    geo: Optional[Geo] = None
    """Gets or Sets Geo"""
    hasBathhouse: Optional[bool] = None
    """Есть баня"""
    hasBathtub: Optional[bool] = None
    """Есть ванна"""
    hasConditioner: Optional[bool] = None
    """Есть кондиционер"""
    hasDishwasher: Optional[bool] = None
    """Есть посудомоечная машина"""
    hasDrainage: Optional[bool] = None
    """Есть канализация"""
    hasElectricity: Optional[bool] = None
    """Есть электричество"""
    hasEncumbrances: Optional[bool] = None
    """Есть обременение"""
    hasEquipment: Optional[bool] = None
    """Есть оборудование"""
    hasExtinguishingSystem: Optional[bool] = None
    """Есть система пожаротушения"""
    hasFridge: Optional[bool] = None
    """Есть холодильник"""
    hasFurniture: Optional[bool] = None
    """Есть мебель в комнатах"""
    hasGarage: Optional[bool] = None
    """Есть гараж"""
    hasGas: Optional[bool] = None
    """Есть газ"""
    hasHeating: Optional[bool] = None
    """Есть отопление"""
    hasInternet: Optional[bool] = None
    """Есть интернет"""
    hasInvestmentProject: Optional[bool] = None
    """Есть инвестпроект"""
    hasKitchenFurniture: Optional[bool] = None
    """Есть мебель на кухне"""
    hasLift: Optional[bool] = None
    """Есть лифт"""
    hasLight: Optional[bool] = None
    """Есть свет"""
    hasParking: Optional[bool] = None
    """Есть парковка"""
    hasPhone: Optional[bool] = None
    """Есть телефон"""
    hasPool: Optional[bool] = None
    """Есть бассейн"""
    hasRamp: Optional[bool] = None
    """Пандус"""
    hasSafeCustody: Optional[bool] = None
    """Ответственное хранение"""
    hasSecurity: Optional[bool] = None
    """Есть охрана"""
    hasShopWindows: Optional[bool] = None
    """Витринные окна"""
    hasShower: Optional[bool] = None
    """Есть душевая кабина"""
    hasTransportServices: Optional[bool] = None
    """Транспортные услуги"""
    hasTv: Optional[bool] = None
    """Есть телевизор"""
    hasWasher: Optional[bool] = None
    """Есть стиральная машина"""
    hasWater: Optional[bool] = None
    """Есть водоснабжение"""
    homeOwner: Optional[HomeOwner] = None
    """Информация о собственнике"""
    id: Optional[int] = None
    """ID объявления в Realty"""
    inputType: Optional[InputType] = None
    """Вход"""
    isApartments: Optional[bool] = None
    """Апартаменты"""
    isByHomeOwner: Optional[bool] = None
    """Собственник объявления"""
    isCustoms: Optional[bool] = None
    """Таможня"""
    isEnabledCallTracking: Optional[bool] = None
    """Флаг, показывающий включен ли calltracking"""
    isInHiddenBase: Optional[bool] = None
    """Размещение в закрытой базе"""
    isLegalAddressProvided: Optional[bool] = None
    """Юридический адрес"""
    isOccupied: Optional[bool] = None
    """Помещение занято"""
    isPenthouse: Optional[bool] = None
    """Пентхаус"""
    isRentByParts: Optional[bool] = None
    """Сдается ли в аренду частями"""
    isSecret: Optional[bool] = None
    """Объявление в закрытую базу только для специалистов"""
    kitchenArea: Optional[float] = None
    """Площадь кухни, м²"""
    kp: Optional[Kp] = None
    """Коттеджный поселок"""
    land: Optional[Land] = None
    """Информация об участке"""
    layout: Optional[Layout] = None
    """Планировка"""
    layoutPhoto: Optional[Photo] = None
    ' Планировка.<br />\r\n LayoutPhoto - изображение планировки, если указан isDefault = true, то всегда идет первым. Если указан isDefault = false, фото планировки будет вторым, а первым установится фото со значением isDefault = true тэга Photos. Фото с установленным IsDefault = true всегда перемещается на первое место, а остальные фотографии отображаются в соответствии с порядком, указанным в объявлении. IsDefault = true может быть установлен только для одного Photo или LayoutPhoto.\r\n<a href="https://www.cian.ru/help/quality/qualityrules/">Требования к изображениям.</a>'
    livingArea: Optional[float] = None
    """Жилая площадь, м²"""
    loggiasCount: Optional[int] = None
    """Количество лоджий"""
    maxArea: Optional[float] = None
    """Площадь до"""
    minArea: Optional[float] = None
    """Площадь от"""
    monthlyIncome: Optional[MonthlyIncome] = None
    """Месячная прибыль"""
    name: Optional[str] = None
    """Наименование"""
    objectGuid: Optional[str] = None
    """Временный ID объявления (GUID)"""
    permittedUseType: Optional[PermittedUseType] = None
    """Вид разрешённого использования"""
    petsAllowed: Optional[bool] = None
    """Можно с животными"""
    phoneLinesCount: Optional[int] = None
    """Кол-во телефонных линий"""
    photos: Optional[List[Photo]] = None
    """Фотографии объекта"""
    placementType: Optional[PlacementType] = None
    """Тип помещения"""
    platform: Optional[Platform] = None
    """Источник последних изменений"""
    possibleToChangePermittedUseType: Optional[bool] = None
    """Возможно изменить вид разрешённого использования"""
    projectDeclarationUrl: Optional[str] = None
    """Проектная декларация"""
    propertyType: Optional[PropertyType] = None
    """Тип недвижимости"""
    publishTerms: Optional[PublishTerms] = None
    """Условия размещения объявления"""
    publishedUserId: Optional[int] = None
    """ID пользователя в Realty от имени которого оно отображается"""
    rentByPartsDescription: Optional[str] = None
    """Описание сдачи части в аренду"""
    repairType: Optional[RepairType] = None
    """Тип ремонта"""
    roomArea: Optional[float] = None
    """Площадь комнаты (комната, койко-место)"""
    roomType: Optional[RoomType] = None
    """Тип комнаты (комната)"""
    roomsArea: Optional[float] = None
    """Площадь комнат, м²"""
    roomsCount: Optional[int] = None
    """Количество комнат всего"""
    roomsForSaleCount: Optional[int] = None
    """Количество комнат в продажу/аренду"""
    rowVersion: Optional[int] = None
    """Версия объявления."""
    separateWcsCount: Optional[int] = None
    """Количество раздельных санузлов"""
    settlementName: Optional[str] = None
    """Название коттеджного поселка"""
    shareAmount: Optional[str] = None
    """Размер доли в доме"""
    source: Optional[Source] = None
    """Источник объявления"""
    specialty: Optional[CommercialSpecialty] = None
    """Возможное назначение"""
    status: Optional[Status] = None
    """Статус объявления"""
    storeInHiddenBase: Optional[bool] = None
    """Размещение в закрытой базе"""
    taxNumber: Optional[int] = None
    """Номер налоговой"""
    title: Optional[str] = None
    """Заголовок объявления. Отображается только для объявлений Премиум и ТОП. Максимальная длина - 33 символа. Минимальная - 8 символов без знаков препинания и пробелов."""
    totalArea: Optional[float] = None
    """Общая площадь, м²"""
    userId: Optional[int] = None
    """ID пользователя в Realty"""
    version: Optional[int] = None
    """Версия модели. Используется для миграции данных."""
    videos: Optional[List[Video]] = None
    """Видео"""
    water: Optional[Water] = None
    """Водоснабжение"""
    waterCapacity: Optional[int] = None
    """Объем, м³/сутки"""
    waterPipesCount: Optional[int] = None
    """Количество мокрых точек (водопровод)"""
    waterType: Optional[WaterType] = None
    """Тип водоснабжения"""
    wcLocationType: Optional[WcLocationType] = None
    """Расположение санузла"""
    wcType: Optional[WcType] = None
    """Тип санузла (комната)"""
    windowsViewType: Optional[WindowsViewType] = None
    """Куда выходят окна"""
