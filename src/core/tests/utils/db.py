import alembic.command
import alembic.config
from sqlalchemy.ext.asyncio import AsyncConnection


def upgrade_database(
    connection: AsyncConnection,
    alembic_config: alembic.config.Config,
) -> None:
    alembic_config.attributes["connection"] = connection
    alembic.command.upgrade(
        config=alembic_config,
        revision="head",
    )
