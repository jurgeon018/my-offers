from my_offers.repositories.monolith_cian_announcementapi.entities import ObjectModel


def get_is_test(object_model: ObjectModel) -> bool:
    return (
        object_model.platform
        and object_model.platform.type
        and object_model.platform.type.is_qa_autotests
    )
