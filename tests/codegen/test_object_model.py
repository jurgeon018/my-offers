from cian_schemas import EntitySchema

from my_offers.repositories.monolith_cian_announcementapi.entities import BargainTerms, ObjectModel, Phone


class PhoneSchema(EntitySchema):
    class Meta:
        entity = Phone


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
            'country_code': None,
            'number': None,
            'source_phone': None,
        }

        # act
        data, errors = PhoneSchema().dumps(data)

        # assert
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
