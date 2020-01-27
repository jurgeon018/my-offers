from cian_enum import Enum, Value


class Category(Enum):
    """Категория объявления"""
    # todo: переделать на StrEnums

    flat_sale = Value(1, help='Продажа квартиры')
    room_sale = Value(2, help='Продажа комнаты')
    new_building_flat_sale = Value(3, help='Продажа квартиры в новостройке')
    flat_share_sale = Value(4, help='Продажа доли в квартире')
    house_sale = Value(5, help='Продажа дома/дачи')
    cottage_sale = Value(6, help='Продажа коттеджа')
    townhouse_sale = Value(7, help='Продажа таунхауса')
    house_share_sale = Value(8, help='Продажа части дома')
    land_sale = Value(9, help='Продажа участка')

    flat_rent = Value(10, help='Аренда квартиры')
    room_rent = Value(11, help='Аренда комнаты')
    bed_rent = Value(12, help='Аренда койко-места')
    house_rent = Value(13, help='Аренда дома/дачи')
    cottage_rent = Value(14, help='Аренда коттеджа')
    townhouse_rent = Value(15, help='Аренда таунхауса')
    house_share_rent = Value(16, help='Аренда части дома')

    daily_flat_rent = Value(17, help='Посуточная аренда квартиры')
    daily_room_rent = Value(18, help='Посуточная аренда комнаты')
    daily_bed_rent = Value(19, help='Посуточная аренда койко-места')
    daily_house_rent = Value(20, help='Посуточная аренда дома, дачи, коттеджа')

    office_sale = Value(21, help='Продажа офиса')
    warehouse_sale = Value(22, help='Продажа склада')
    shopping_area_sale = Value(23, help='Продажа торговой площади')
    industry_sale = Value(24, help='Продажа производство')
    building_sale = Value(25, help='Продажа здания')
    free_appointment_object_sale = Value(26, help='Продажа помещения свободного назначения')
    business_sale = Value(27, help='Продажа готового бизнеса')
    commercial_land_sale = Value(28, help='Продажа коммерческой земли')
    garage_sale = Value(29, help='Продажа гаража')

    office_rent = Value(30, help='Аренда офиса')
    warehouse_rent = Value(31, help='Аренда склада')
    shopping_area_rent = Value(32, help='Аренда торговой площади')
    industry_rent = Value(33, help='Аренда производства')
    building_rent = Value(34, help='Аренда здания')
    free_appointment_object_rent = Value(35, help='Аренда помещения свободного назначения')
    business_rent = Value(36, help='Аренда готового бизнеса')
    commercial_land_rent = Value(37, help='Аренда коммерческой земли')
    garage_rent = Value(38, help='Аренда гаража')
    # region v1
    public_catering_sale = Value(39, help='Продажа общепита')
    car_service_sale = Value(40, help='Продажа автосервиса')
    domestic_services_sale = Value(41, help='Продажа помещения под бытовые услуги')

    public_catering_rent = Value(42, help='Аренда общепита')
    car_service_rent = Value(43, help='Аренда автосервис')
    domestic_services_rent = Value(44, help='Аренда помещения под бытовые услуги')
