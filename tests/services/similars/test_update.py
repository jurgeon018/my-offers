from my_offers.repositories.monolith_cian_announcementapi.entities.platform import Type
from my_offers.services.similars._update import get_similar_table_suffix


def test_get_similar_table_suffix__test__test(mocker):
    # arrange
    object_model = mocker.sentinel.object_model
    object_model.platform = mocker.sentinel.platform
    object_model.platform.type = Type.qa_autotests

    # act
    result = get_similar_table_suffix(object_model)

    # assert
    assert result == 'test'
