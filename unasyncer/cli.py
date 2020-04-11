"""CLI for unasyncer with Typer"""

import pathlib
from typing import List

import typer

from unasyncer.unasync import unasync_path

try:  # pragma: no cover
    from importlib.metadata import version  # noqa: WPS433
except ImportError:  # pragma: no cover
    from importlib_metadata import version  # type: ignore  # noqa: WPS433, WPS440


cli = typer.Typer()


def version_callback(show_version: bool) -> None:
    if show_version:
        unasyncer_version = version("unasyncer")
        typer.echo(f"unasyncer {unasyncer_version}")
        raise typer.Exit()


@cli.command(hidden=True)
def unasync(
    paths: List[pathlib.Path] = typer.Argument(..., exists=True),  # noqa: WPS404
    prefix: str = typer.Option(
        "",
        "--prefix",
        "-p",
        help='Replace "async" prefix with passed one for code entities.',
        show_default=True,
    ),
    unasync_root_prefix: str = typer.Option(
        "_sync",
        "--root-prefix",
        help="Prefix for unasynced root path.",
        show_default=True,
    ),
    create_folders: bool = typer.Option(
        True,  # noqa: WPS425
        "--create-folders/--no-folders",
        help="Create recursive paths for unasynced code.",
        show_default=True,
    ),
    _version: bool = typer.Option(
        False, "--version", "-v", callback=version_callback,  # noqa: WPS425
    ),
) -> None:
    """unasyncer - CLI to "unasync" your python code."""
    for path in paths:
        try:
            unasyncer = unasync_path(
                path, path.parent / unasync_root_prefix, prefix, create_folders,
            )
        except ValueError as not_file_error:
            typer.echo(str(not_file_error), err=True)
            raise typer.Exit(2)

        try:
            for processed_path in unasyncer:
                typer.echo(f"processed: {processed_path}")
        except RuntimeError as error:
            typer.echo(str(error), err=True)
            raise typer.Exit(2)

    typer.echo("unasyncing completed!")
