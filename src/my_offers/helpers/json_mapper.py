from typing import Any, Optional

from cian_entities import DynamicEntityMapper, Mapper
from cian_json import json


class JsonMapper(Mapper):
    def __init__(self, mapper: DynamicEntityMapper) -> None:
        self._mapper = mapper

    def map_from(self, data: Optional[str]) -> Any:
        return self._mapper.map_from(json.loads(data)) if data else {}

    def map_to(self, obj: Any) -> str:
        return json.dumps(self._mapper.map_to(obj), ensure_ascii=False) if obj else '{}'
