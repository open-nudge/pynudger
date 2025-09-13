# SPDX-FileCopyrightText: © 2025 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Smoke test CLI entrypoint."""

from __future__ import annotations

import typing

import lintkit

import pytest

from pynudger import _cli


@pytest.mark.parametrize(
    "command",
    (
        ["rules"],
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
    try:
        _cli.main(args=command)
    except SystemExit as e:
        if command[0] == "check":
            out, _ = capsys.readouterr()
            for i in lintkit.registry.codes():
                assert f"PYNUDGER{i}" in out
        else:
            assert e.code == 0  # noqa: PT017
