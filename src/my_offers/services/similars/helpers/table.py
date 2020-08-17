from my_offers.helpers import fields
from my_offers.repositories.monolith_cian_announcementapi.entities import ObjectModel


def get_similar_table_suffix(object_model: ObjectModel) -> str:
    if fields.is_test(object_model):
        return 'test'

    return 'flat'


def get_similar_table_suffix_by_params(is_test: bool) -> str:
    if is_test:
        return 'test'

    return 'flat'
