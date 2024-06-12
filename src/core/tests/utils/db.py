import alembic.command
import alembic.config
from sqlalchemy import Connection


def upgrade_database(
    connection: Connection,
    alembic_config: alembic.config.Config,
) -> None:
    alembic_config.attributes["connection"] = connection
    alembic.command.upgrade(
        config=alembic_config,
        revision="head",
    )
