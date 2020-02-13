from my_offers.repositories.monolith_cian_announcementapi.entities.address_info import Type as GeoType


FIELDS_FOR_EXCLUDE = (
    'id_suburbian',
    'id_flat',
    'id_office',
    'bs_center_id',
    'id_user',
    'multi_id',
    'show_inactive',
    'builders',
    'p',
    'polygon_name',
)


ALL_GEO_KEYS = (
    'locations',
    'district',
    'id_metro',
    'distance',
    'polygon',
    'foot_min',
    'only_foot',
    'newobject',
    'NewObjectId',
    'region',
)


GEO_KEYS_MAP = {
    GeoType.location: 'location',
    GeoType.street: 'street',
    GeoType.road: 'highway',
    GeoType.district: 'district',
    GeoType.underground: 'metro',
    GeoType.house: 'house',

    # todp: разобраться с этим
    # GeoType.mikroraion: 'district',
    # GeoType.poselenie: 'district',
    # GeoType.okrug: 'district',
    # GeoType.raion: 'district',
    # GeoType.metro: 'metro',
}
