# SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Smoke test CLI entrypoint."""

from __future__ import annotations

import pathlib
import typing

import lintkit

import pytest

from pynudger import _cli


@pytest.mark.parametrize(
    "command",
    (
        ["rules"],
        ["check"],
        [
            "check",
            "./tests/test_cases/common.py",
            "./tests/test_cases/getters.py",
            "./tests/test_cases/helper.py",
            "./tests/test_cases/setters.py",
            "./tests/test_cases/util.py",
            "./tests/test_cases/mixed.py",
            "./tests/test_cases/very_long_filename_definitely_too_long.py",
        ],
    ),
)
def test_cli(
    command: list[str],
    capsys: typing.Any,
) -> None:
    """Smoke test pynudger CLI.

    Args:
        command:
            Command to test. One of `rules` or `check`.
        capsys:
            Pytest system capture fixture (used for stdout/stderr analysis).

    """
    if command[0] == "check" and len(command) > 1:
        command = [*command, str(_restricted_path())]

    try:
        _cli.main(args=command)
    except SystemExit as e:
        if command[0] == "check":
            out, _ = capsys.readouterr()
            for i in lintkit.registry.codes():
                assert f"PYNUDGER{i}" in out
        else:
            assert e.code == 0  # noqa: PT017


def _restricted_path() -> pathlib.Path:
    """Return the restricted runtime construct fixture path.

    Returns:
        Resolved restricted runtime construct fixture path.

    """
    return pathlib.Path("tests/test_cases/restricted.py").resolve()
