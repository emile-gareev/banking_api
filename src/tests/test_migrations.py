import os
import pytest
from alembic import command
from alembic.config import Config
from alembic.script import Script, ScriptDirectory
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession


pytestmark = pytest.mark.asyncio


def get_alembic_config() -> Config:
    base_dir = Path(__file__).resolve().parent.parent
    return Config(os.path.join(base_dir, "alembic.ini"))


def get_revisions() -> list[Script]:
    alembic_cfg = get_alembic_config()
    revisions_dir = ScriptDirectory.from_config(alembic_cfg)
    revisions = list(revisions_dir.walk_revisions("base", "heads"))
    revisions.reverse()

    return revisions


@pytest.fixture()
def alembic_config() -> Config:
    return get_alembic_config()


# @pytest.mark.skip(reason="Connect to work db and drop data.")
@pytest.mark.parametrize("revision", get_revisions())
def test_ok(
    db_session: AsyncSession,
    alembic_config: Config,
    revision: Script,
) -> None:
    command.upgrade(alembic_config, revision.revision)

    command.downgrade(alembic_config, revision.down_revision or "-1")
    command.upgrade(alembic_config, revision.revision)
