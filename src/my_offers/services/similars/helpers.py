from my_offers.helpers.fields import is_test
from my_offers.repositories.monolith_cian_announcementapi.entities import ObjectModel


def get_similar_table_suffix(object_model: ObjectModel) -> str:
    if is_test(object_model):
        return 'test'

    return 'flat'
