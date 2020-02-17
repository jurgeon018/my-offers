import typing

import cian_core
from cian_core.registry import postgres_connections


if typing.TYPE_CHECKING:
    from cian_core.postgres import PostgresConnection
    from cian_core.registry.base import Value

pg: 'Value[PostgresConnection]' = postgres_connections('my_offers')


def setup() -> None:
    cian_core.setup(
        options=cian_core.Options(
            setup_postgres=True,
            setup_redis=True,
        )
    )
