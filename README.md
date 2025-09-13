<!--
SPDX-FileCopyrightText: © 2025 open-nudge <https://github.com/open-nudge>
SPDX-FileContributor: szymonmaszke <github@maszke.co>

SPDX-License-Identifier: Apache-2.0
-->

# pynudger

<!-- mkdocs remove start -->

<!-- vale off -->

<!-- pyml disable-num-lines 30 line-length-->

<p align="center">
    <em>opennudge Python linter (naming conventions and other automated checks)</em>
</p>

<div align="center">

<a href="https://pypi.org/project/pynudger">![PyPI - Python Version](https://img.shields.io/pypi/v/pynudger?style=for-the-badge&label=release&labelColor=grey&color=blue)
</a>
<a href="https://pypi.org/project/pynudger">![Python Version from PEP 621 TOML](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2Fopen-nudge%2Fpynudger%2Fmain%2Fpyproject.toml&style=for-the-badge&label=python&labelColor=grey&color=blue)
</a>
<a href="https://opensource.org/licenses/Apache-2.0">![License](https://img.shields.io/badge/License-Apache_2.0-blue?style=for-the-badge)
</a>
<a>![Coverage Hardcoded](https://img.shields.io/badge/coverage-100%25-green?style=for-the-badge)
</a>
<a href="https://scorecard.dev/viewer/?uri=github.com/open-nudge/pynudger">![OSSF-Scorecard Score](https://img.shields.io/ossf-scorecard/github.com/open-nudge/pynudger?style=for-the-badge&label=OSSF)
</a>

</div>

<p align="center">
✨ <a href="#features">Features</a>
🚀 <a href="#quick-start">Quick start</a>
📚 <a href="https://open-nudge.github.io/pynudger">Documentation</a>
🤝 <a href="#contribute">Contribute</a>
👍 <a href="https://github.com/open-nudge/pynudger/blob/main/ADOPTERS.md">Adopters</a>
📜 <a href="#legal">Legal</a>
</p>
<!-- vale on -->

______________________________________________________________________

<!-- mkdocs remove end -->

## Features

__pynudger__ is an opinionated linter for Python projects, focused on
naming conventions and making your code "more Pythonic".

- __Length rules__: Too long class/function names are flagged.
- __Setters/getters__: Discourages usage of setters/getters,
    encourages properties instead.
- __No helpers/utils/commons__: Incentivizes more descriptive
    and semantically coherent names for functionalities.

## Table of contents

- [Quick start](#quick-start)
    - [Installation](#installation)
    - [Usage](#usage)
- [Advanced](#advanced)
    - [Configuration](#configuration)
    - [Run as a pre-commit hook](#run-as-a-pre-commit-hook)
    - [Disable in code](#disable-in-code)
    - [Rules](#rules)

## Quick start

### Installation

> [!TIP]
> You can use your favorite package manager like
> [`uv`](https://github.com/astral-sh/uv),
> [`hatch`](https://github.com/pypa/hatch)
> or [`pdm`](https://github.com/pdm-project/pdm)
> instead of `pip`.

```sh
> pip install pynudger
```

### Usage

To check against the rules run the following from the command line:

```sh
> pynudger check
```

You can pass additional arguments to `pynudger check`, like files
to check (by default all Python files in the current directory):

```sh
> pynudger check path/to/file.py another_file.py
```

## Advanced

### Configuration

You can configure pynudger in `pyproject.toml` (or `.pynudger.toml`
in the root of your project, just remove the `[tool.pynudger]` section),
for example:

```toml
[tool.pynudger]
# include rules by their code
include_codes = [1, 2, 5] # default: all rules included
# exclude rules by their code (takes precedence over include)
exclude_codes = [4, 5, 6] # default: no rules excluded
# whether to exit after first error or all errors
end_mode = "first" # default: "all"
```

> [!TIP]
> Rule-specific configuration can be found in the section below.

### Run as a pre-commit hook

`pynudger` can be used as a pre-commit hook, to add as a plugin:

```yaml
repos:
-   repo: "https://github.com/open-nudge/pynudger"
    rev: ...  # select the tag or revision you want, or run `pre-commit autoupdate`
    hooks:
    -   id: "pynudger"
```

### Disable in code

You can disable `pynudger` on a line-by-line basis
(you have to specify exact code), e.g.:

```python
def set_my_too_long_function_name():  # noqa: PYNUDGER0, PYNUDGER16
    pass
```

or a line span:

```python
# noqa-start: PYNUDGER0, PYNUDGER16
def set_my_too_long_function_name():
    pass

def set_another_long_function():
    pass
# noqa-end: PYNUDGER0, PYNUDGER16

def set_will_error_out_this_time():
    pass
```

It is also possible to disable all checks in a file
by placing the following somewhere in the file (preferably at the top):

```python
# noqa-file: PYNUDGER0, PYNUDGER16
```

> [!NOTE]
> If you are running `pynudger` with
> [`ruff`](https://github.com/astral-sh/ruff) you should add
> `lint.external = ["PYNUDGER"]` to `[tool.ruff]` section in
> `pyproject.toml` to avoid removing `# noqa: PYNUDGER` comments.

### Rules

> [!TIP]
> Run `pynudger rules` to see the list of available rules.

`pynudger` provides the following rules:

<!-- pyml disable-num-lines 25 line-length-->

| Name         | Description                                                               |
| ------------ | ------------------------------------------------------------------------- |
| `PYNUDGER0`  | Avoid using setters in class names. Use properties instead.               |
| `PYNUDGER1`  | Avoid using setters in function names. Use properties instead.            |
| `PYNUDGER2`  | Avoid using setters in file names. Define file name without it.           |
| `PYNUDGER3`  | Avoid using getters in class names. Use properties instead.               |
| `PYNUDGER4`  | Avoid using getters in function names. Use properties instead.            |
| `PYNUDGER5`  | Avoid using getters in file names. Define file name without it.           |
| `PYNUDGER6`  | Avoid using utils in class names. Name the class appropriately.           |
| `PYNUDGER7`  | Avoid using utils in function names. Name the function appropriately.     |
| `PYNUDGER8`  | Avoid defining utils modules. Move functionality to appropriate modules.  |
| `PYNUDGER9`  | Avoid using helpers in class names. Name the class appropriately.         |
| `PYNUDGER10` | Avoid using helpers in function names. Name the function appropriately.   |
| `PYNUDGER11` | Avoid defining utils modules. Move functionality to appropriate modules.  |
| `PYNUDGER12` | Avoid using common in class names. Name the class appropriately.          |
| `PYNUDGER13` | Avoid using common in function names. Name the function appropriately.    |
| `PYNUDGER14` | Avoid defining common modules. Move functionality to appropriate modules. |
| `PYNUDGER15` | Avoid long class names. Specify intent by nesting modules/packages.       |
| `PYNUDGER16` | Avoid long function names. Specify intent by nesting modules/packages.    |
| `PYNUDGER17` | Avoid long path names. Specify intent by nesting modules/packages.        |

with the following configurable options (in `pyproject.toml`
or `.pynudger.toml`):

<!-- pyml disable-num-lines 10 line-length-->

| Option            | Description                                           | Affected rules         | Default |
| ----------------- | ----------------------------------------------------- | ---------------------- | ------- |
| `pascal_length`   | Maximum allowed length of PascalCase names            | PYNUDGER15             | 3       |
| `snake_length`    | Maximum allowed length of snake_case names            | PYNUDGER16, PYNUDGER17 | 3       |
| `pascal_excludes` | List of words to exclude from PascalCase length check | PYNUDGER15             | []      |
| `snake_excludes`  | List of words to exclude from snake_case length check | PYNUDGER16, PYNUDGER17 | []      |

## Contribute

<!-- md-dead-link-check: off -->

<!-- mkdocs remove start -->

We welcome your contributions! Start here:

- [Code of Conduct](/CODE_OF_CONDUCT.md)
- [Contributing Guide](/CONTRIBUTING.md)
- [Roadmap](/ROADMAP.md)
- [Changelog](/CHANGELOG.md)
- [Report security vulnerabilities](/SECURITY.md)
- [Open an Issue](https://github.com/open-nudge/pynudger/issues)

## Legal

- This project is licensed under the _Apache 2.0 License_ - see
    the [LICENSE](/LICENSE.md) file for details.
- This project is copyrighted by _open-nudge_ - the
    appropriate copyright notice is included in each file.

<!-- mkdocs remove end -->

<!-- md-dead-link-check: on -->
