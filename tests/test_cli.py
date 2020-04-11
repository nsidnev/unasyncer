import os
import pathlib

import pytest
import toml
from typer.testing import CliRunner

from unasyncer.cli import cli


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


def test_version_callback(runner: CliRunner) -> None:
    with open(pathlib.Path(__file__).parent.parent / "pyproject.toml") as manifest_file:
        manifest = toml.load(manifest_file)

    result = runner.invoke(cli, ["--version"])

    assert result.exit_code == 0
    assert f"unasyncer {manifest['tool']['poetry']['version']}" in result.stdout


class TestUnasyncing:
    def test_unasyncing_without_params(
        self, runner: CliRunner, sources: pathlib.Path
    ) -> None:
        async_folder = sources / "_async"
        sync_folder = sources / "_sync"

        result = runner.invoke(cli, [str(async_folder)])

        required_paths = [
            sync_folder / "__init__.py",
            sync_folder / "inner_package",
            sync_folder / "inner_package" / "__init__.py",
            sync_folder / "inner_package" / "logic.py",
        ]

        assert result.exit_code == 0

        for path in required_paths:
            assert path.exists()

        assert "unasyncing completed" in result.stdout

    def test_unasyncing_with_custom_sync_code_prefix(
        self, runner: CliRunner, sources: pathlib.Path
    ) -> None:
        prefix = "sync_code"
        async_folder = sources / "_async"
        sync_folder = sources / prefix

        result = runner.invoke(cli, [f"--root-prefix", prefix, str(async_folder)])

        required_paths = [
            sync_folder / "__init__.py",
            sync_folder / "inner_package",
            sync_folder / "inner_package" / "__init__.py",
            sync_folder / "inner_package" / "logic.py",
        ]

        assert result.exit_code == 0

        for path in required_paths:
            assert path.exists()

        assert "unasyncing completed" in result.stdout

    def test_error_when_start_path_does_not_exist(
        self, runner: CliRunner, sources: pathlib.Path
    ) -> None:
        fifo_path = sources / "fifo"

        os.mkfifo(fifo_path)

        result = runner.invoke(cli, [str(fifo_path)])

        assert result.exit_code == 2

    def test_error_when_path_does_not_exist_and_creation_disabled(
        self, runner: CliRunner, sources: pathlib.Path
    ) -> None:
        async_folder = sources / "_async"

        result = runner.invoke(cli, ["--no-folders", str(async_folder)])

        assert result.exit_code == 2
