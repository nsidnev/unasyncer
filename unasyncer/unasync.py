"""Core of unasync logic."""

import pathlib
import re
from typing import Iterator, List, Pattern, Tuple

_DEFAULT_SUBS = (
    ("async def", "def"),
    ("async with", "with"),
    ("async for", "for"),
    ("await ", ""),
    ("__aenter__", "__enter__"),
    ("__aexit__", "__exit__"),
    ("__aiter__", "__iter__"),
    ("@pytest.mark.asyncio", ""),
)


def _subs_for_replacement(prefix: str) -> Tuple[Tuple[str, str], ...]:
    return (
        (r"Async([A-Z][A-Za-z0-9_]*)", r"{0}\g<2>".format(prefix.capitalize())),
        (r"async_([a-z][A-Za-z0-9_]*)", r"{0}\g<2>".format(prefix.lower())),
    ) + _DEFAULT_SUBS


def _compile_regexes(prefix: str) -> List[Tuple[Pattern, str]]:
    return [
        (re.compile(r"(^|\b){0}($|\b)".format(regex)), repl)
        for regex, repl in _subs_for_replacement(prefix)
    ]


def _unasync_line(line: str, prefix: str) -> str:
    for regex, repl in _compile_regexes(prefix):
        line = re.sub(regex, repl, line)
    return line


# this is iterator for interface consistety
def _unasync_file(
    input_path: pathlib.Path,
    out_path: pathlib.Path,
    prefix: str,
    create_missed_path: bool,
) -> Iterator[pathlib.Path]:
    if input_path.suffix != ".py":
        return

    out_parent_dir = out_path.parent
    if not (out_parent_dir.exists() or create_missed_path):
        raise RuntimeError(
            "directory {0} for file does not exist and creation disabled".format(
                out_parent_dir,
            ),
        )

    out_parent_dir.mkdir(parents=True, exist_ok=True)

    with open(input_path) as input_file:
        with open(out_path, "w") as out_file:
            for line in input_file:
                out_file.write(_unasync_line(line, prefix))

    yield out_path


def _unasync_dir(
    input_dir: pathlib.Path,
    out_dir: pathlib.Path,
    prefix: str,
    create_missed_paths: bool,
) -> Iterator[pathlib.Path]:
    for path in input_dir.iterdir():
        if path.is_dir():
            yield from _unasync_dir(
                path, out_dir / path.name, prefix, create_missed_paths,
            )
        elif path.is_file():
            yield from _unasync_file(
                path, out_dir / path.name, prefix, create_missed_paths,
            )


def unasync_path(
    input_path: pathlib.Path,
    out_path: pathlib.Path,
    prefix: str = "",
    create_missed_paths: bool = True,
) -> Iterator[pathlib.Path]:
    """Iterate over directory or file and unasync it's content.

    Arguments:
        input_path: path to file or directory that should be unasynced.
        out_path: path where to store unasynced code.
        prefix: prefix for replacement "async" word in entities.
        create_missed_paths: create paths if they don't exist.

    Information:
        `prefix` will replace entities in following way:
        1. `async def async_function():` to `def function():`.
        2. `class AsyncClass:` to `class Class`.

    Raises:
        FileNotFoundError: if passed input_file does not exist.
        ValueError: if passed input_path is not a file or directory.

    Returns:
        Iterator that yields processed file paths.
    """
    if not input_path.exists():
        raise FileNotFoundError(f"path {0} does not exist".format(input_path))

    if input_path.is_dir():
        return _unasync_dir(input_path, out_path, prefix, create_missed_paths)
    elif input_path.is_file():
        return _unasync_file(
            input_path, out_path.with_suffix(".py"), prefix, create_missed_paths,
        )

    raise ValueError("{0} is not a directory or file".format(input_path))
