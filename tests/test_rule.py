# SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Test rule violations detection."""

from __future__ import annotations

import typing

import lintkit

import pytest

from pynudger import _cli


@pytest.mark.parametrize(
    ("cases", "clean"),
    (
        ("./tests/cases/clean", True),
        ("./tests/cases/violations", False),
    ),
)
def test_rules(
    cases: str,
    clean: bool,  # noqa: FBT001
    capsys: typing.Any,
) -> None:
    """Test rule violations detection.

    Args:
        cases:
            Path to the test case directory containing Python files.
        clean:
            Whether the test case is expected to be clean (True) or
            contain violations (False).
        capsys:
            Pytest system capture fixture (used for stdout/stderr analysis).

    """
    try:
        _cli.main(args=["check"], path=cases)
    except SystemExit:
        out, _ = capsys.readouterr()
        for i in lintkit.registry.codes():
            rule = f"{lintkit.settings.name}{i} "
            if not clean:
                # Check a single violation is returned to make sure
                # each violation was not accidentally created
                assert out.count(rule) == 1
            else:
                assert rule not in out
