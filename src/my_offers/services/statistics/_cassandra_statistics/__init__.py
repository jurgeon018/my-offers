from ._base import BaseStatCassandraRepository
from ._coverage import CoverageCassandraRepository
from ._search_coverage import SearchCoverageCassandraRepository
from ._views import ViewsCassandraRepository


base_cs_repo = BaseStatCassandraRepository()
coverage_cs_repo = CoverageCassandraRepository()
search_coverage_cs_repo = SearchCoverageCassandraRepository()
views_cs_repo = ViewsCassandraRepository()
