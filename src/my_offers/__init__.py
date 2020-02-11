import typing

import cian_core
from cian_core.postgres.setup import SetupPostgres
from cian_core.registry import postgres_connections


if typing.TYPE_CHECKING:
    from cian_core.postgres import PostgresConnection
    from cian_core.registry.base import Value

pg: 'Value[PostgresConnection]' = postgres_connections('my_offers')


# def _get_connection_settings(self, alias: str):
#     return {
#         "user": "my_offers",
#         "password": "Wgwh6qimgre2oisdxv21",
#         "database": "my_offers",
#         "host": "localhost",
#         "min_size": 1
#     }
#
#
# SetupPostgres._get_connection_settings = _get_connection_settings

def setup() -> None:
    cian_core.setup(
        options=cian_core.Options(
            setup_postgres=True,
        )
    )
