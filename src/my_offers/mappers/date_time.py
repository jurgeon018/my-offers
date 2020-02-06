from cian_entities.mappers import DateTimeMapper
from cian_helpers.timezone import is_naive, make_aware


class DateTimeTimeZoneMapper(DateTimeMapper):
    def map_from(self, data):
        result = super().map_from(data)
        if is_naive(result):
            result = make_aware(result)

        return result


date_time_mapper = DateTimeTimeZoneMapper()
