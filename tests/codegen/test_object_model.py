from cian_schemas import EntitySchema

from my_offers.repositories.monolith_cian_announcementapi.entities import BargainTerms, ObjectModel
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Category


class ObjectModelSchema(EntitySchema):
    class Meta:
        entity = ObjectModel


class BargainTermsSchema(EntitySchema):
    class Meta:
        entity = BargainTerms


class TestCodegenObjectModel:

    def test_phones(self):
        """ У некоторых объявлений не приходит `country_code`
            Читаев:
                Сейчас считайте что он всегда 138, он самовыпилился когда мы отказались от заруюежной недвижимости
        """
        # arrange
        data = {
            'Category': Category.bed_rent.value,
            'bargain_terms': {},
            'phones': [None],
        }

        # act
        data, errors = ObjectModelSchema().dumps(data)

        # assert
        assert data == '{"phones": [{}], "bargainTerms": {}}'
        assert not errors

    def test_bargain_terms_price(self):
        """ У старых объявлений может отсутвовать `price`
        """
        # arrange
        data = {
            'price': None
        }

        # act
        data, errors = BargainTermsSchema().dumps(data)

        # assert
        assert not errors
