<h1 align="center">unasyncer</h1>
<p align="center">
    <em>CLI to "unasync" your python code.</em>
</p>
<p align="center">
    <a href=https://github.com/nsidnev/unasyncer>
        <img src=https://github.com/nsidnev/unasyncer/workflows/Tests/badge.svg alt="Tests" />
    </a>
    <a href=https://github.com/nsidnev/unasyncer>
        <img src=https://github.com/nsidnev/unasyncer/workflows/Styles/badge.svg alt="Styles" />
    </a>
    <a href="https://codecov.io/gh/nsidnev/unasyncer">
        <img src="https://codecov.io/gh/nsidnev/unasyncer/branch/master/graph/badge.svg" alt="Coverage" />
    </a>
    <a href="https://github.com/ambv/black">
        <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code Style" />
    </a>
    <a href="https://github.com/wemake-services/wemake-python-styleguide">
        <img src="https://img.shields.io/badge/style-wemake-000000.svg" alt="WPS Linter"/>
    </a>
    <a href="https://github.com/nsidnev/edgeql-queries/blob/master/LICENSE">
        <img src="https://img.shields.io/github/license/Naereen/StrapDown.js.svg" alt="License" />
    </a>
</p>

---

## Requirements

`unasyncer` requires [Typer](https://github.com/tiangolo/typer) for processing CLI commands and [importlib-metadata](https://pypi.org/project/importlib-metadata/) for Python 3.6 and 3.7.

## Usage

Let's say your asynchronous code is folded in `library/_async` folder.

To "unasync" it to `library/_sync` run following command:
```bash
unasyncer path-to-code/_async
```

## Credits

This project is inspired by [unasync](https://github.com/python-trio/unasync)
project and use script from [httpcore](https://github.com/encode/httpcore) as base for unasyncing logic.

## License

This project is licensed under the terms of the MIT license.
