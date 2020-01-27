import cian_core
from cian_core.registry import postgres_connections


pg = postgres_connections('my_offers')


def setup() -> None:
    cian_core.setup(
        options=cian_core.Options(
            setup_postgres=True,
        )
    )
