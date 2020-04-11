import os
import pathlib

import pytest

from unasyncer.unasync import unasync_path


@pytest.fixture
def expected_unasynced_code(sources: pathlib.Path) -> str:
    with open(sources / "right_sync.py") as right_sync_file:
        return right_sync_file.read()


def test_create_right_sync_structure_for_dir(sources: pathlib.Path) -> None:
    async_folder = sources / "_async"
    sync_folder = sources / "_sync"

    [_ for _ in unasync_path(async_folder, sync_folder)]  # consume iterator

    required_paths = [
        sync_folder / "__init__.py",
        sync_folder / "inner_package",
        sync_folder / "inner_package" / "__init__.py",
        sync_folder / "inner_package" / "logic.py",
    ]
    for path in required_paths:
        assert path.exists()


def test_create_unasynced_single_file(sources: pathlib.Path) -> None:
    async_file_path = sources / "_async" / "inner_package" / "logic.py"
    sync_file_path = sources / "_async" / "inner_package" / "sync.py"

    next(unasync_path(async_file_path, sync_file_path))

    assert sync_file_path.exists()


def test_unasynced_file_content(
    sources: pathlib.Path, expected_unasynced_code: str
) -> None:
    async_file_path = sources / "_async" / "inner_package" / "logic.py"
    sync_file_path = sources / "_async" / "inner_package" / "sync.py"

    next(unasync_path(async_file_path, sync_file_path))

    with open(sync_file_path) as sync_file:
        content = sync_file.read()

    assert content == expected_unasynced_code


def test_skiping_not_files_or_dirs(sources: pathlib.Path) -> None:
    async_folder = sources / "_async"
    sync_folder = sources / "_sync"

    fifo_path = async_folder / "fifo"

    os.mkfifo(fifo_path)

    [_ for _ in unasync_path(async_folder, sync_folder)]  # consume iterator

    assert not (sync_folder / "fifo").exists()


def test_raising_error_for_not_files_or_dirs_in_unasync_path(
    sources: pathlib.Path,
) -> None:
    async_folder = sources / "_async"
    sync_folder = sources / "_sync"

    fifo_path = async_folder / "fifo"

    os.mkfifo(fifo_path)

    with pytest.raises(ValueError):
        next(unasync_path(fifo_path, sync_folder / "fifo"))


def test_raising_error_if_dir_does_not_exist_and_creation_disabled(
    sources: pathlib.Path,
) -> None:
    async_folder = sources / "_async"
    sync_folder = sources / "_sync"

    with pytest.raises(RuntimeError):
        next(unasync_path(async_folder, sync_folder, create_missed_paths=False))


def test_raising_error_if_path_does_not_exist() -> None:
    with pytest.raises(FileNotFoundError):
        next(unasync_path(pathlib.Path("error_path"), pathlib.Path("_sync")))
