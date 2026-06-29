# SPDX-FileCopyrightText: © 2025 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Tests for restricted runtime construct rules."""

from __future__ import annotations

import pathlib
import typing

import pytest

from pynudger import _cli
from pynudger._restricted import rule


def test_rules_keywords(capsys: typing.Any) -> None:
    """Verify restricted rules list every covered keyword.

    Args:
        capsys:
            Pytest system capture fixture.

    """
    with pytest.raises(SystemExit) as error:
        _cli.main(args=["rules"])

    assert error.value.code == 0
    out, _ = capsys.readouterr()

    for code, keywords in (
        (18, ("del", "global", "nonlocal", "pass")),
        (19, ("break", "continue")),
        (20, ("object", "basestring", "unicode", "long")),
        (21, ("breakpoint", "help", "id")),
        (22, ("typing.cast", "bool", "float", "int", "str")),
        (23, ("exec", "eval", "compile")),
        (24, ("iter", "aiter", "anext", "next")),
        (
            25,
            (
                "delattr",
                "getattr",
                "hasattr",
                "setattr",
                "globals",
                "locals",
                "vars",
                "dir",
                "property",
            ),
        ),
        (26, ("__",)),
    ):
        assert f"PYNUDGER{code}" in out
        for keyword in keywords:
            assert keyword in out


@pytest.mark.parametrize(
    ("check", "keywords"),
    (
        (rule.State(), ("del", "global", "nonlocal", "pass")),
        (rule.IterationKeyword(), ("break", "continue")),
        (rule.Dunder(), ("__*",)),
    ),
)
def test_keyword_methods(check: typing.Any, keywords: tuple[str, ...]) -> None:
    """Verify restricted keyword helpers return display values.

    Args:
        check:
            Restricted rule instance under test.
        keywords:
            Expected restricted keyword display values.

    """
    assert check.keywords() == keywords


def test_restricted_codes(
    capsys: typing.Any,
) -> None:
    """Verify representative restricted runtime constructs emit new codes.

    Args:
        capsys:
            Pytest system capture fixture.

    """
    path = pathlib.Path("tests/test_cases/restricted.py").resolve()

    with pytest.raises(SystemExit) as error:
        _cli.main(args=["check", str(path)])

    assert error.value.code == 1
    out, _ = capsys.readouterr()
    for code in range(18, 27):
        assert f"PYNUDGER{code}" in out


def test_runtime_only(
    capsys: typing.Any,
) -> None:
    """Verify annotations and plain local names are not flagged.

    Args:
        capsys:
            Pytest system capture fixture.

    """
    path = pathlib.Path("tests/test_cases/allowed_runtime.py").resolve()

    with pytest.raises(SystemExit) as error:
        _cli.main(args=["check", str(path)])

    assert error.value.code == 0
    out, _ = capsys.readouterr()
    assert "PYNUDGER20" not in out
    assert "PYNUDGER22" not in out
