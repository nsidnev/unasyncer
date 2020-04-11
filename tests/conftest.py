import pathlib
import shutil
import tempfile

import pytest


@pytest.fixture
def sources() -> pathlib.Path:
    sources_path = pathlib.Path(__file__).parent / "sources"
    directory = pathlib.Path(tempfile.mkdtemp()) / "test"
    shutil.copytree(sources_path, directory)
    return pathlib.Path(directory)
