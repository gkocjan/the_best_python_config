import os
from pathlib import Path

import pytest

from the_best.settings import Settings


@pytest.fixture
def change_working_directory_to_tmp_path(tmp_path):
    prev_cwd = Path.cwd()
    os.chdir(tmp_path)
    yield
    os.chdir(prev_cwd)


def test_dotenv_file_populates_pydantic_settings(
    tmp_path, change_working_directory_to_tmp_path
):
    env_file = tmp_path / ".env"
    env_content = """
DEBUG=true

DB__TYPE=sqlite
DB__PATH=db.sqlite
"""
    env_file.write_text(env_content)

    settings = Settings()

    assert settings.debug is True
    assert settings.db.type == "sqlite"
