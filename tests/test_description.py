# SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Smoke test rule descriptions."""

from __future__ import annotations

import typing

import lintkit

import pytest

from pynudger import _cli


@pytest.mark.parametrize(
    ("args", "names"),
    (
        (["rules"], None),
        (["rules", "--names", "PYNUDGER0"], {"PYNUDGER0"}),
    ),
)
def test_rules(
    capsys: typing.Any, args: list[str], names: set[str] | None
) -> None:
    """Smoke test rules provide descriptions.

    Args:
        capsys:
            Pytest system capture fixture (used for stdout/stderr analysis).
        args:
            CLI arguments for listing all or selected rules.
        names:
            Full rule names to select, or all rules when `None`.

    """
    try:
        _cli.main(args=args)
    except SystemExit:
        out, _ = capsys.readouterr()
        for i in lintkit.registry.codes():
            name = f"{lintkit.settings.name}{i}"
            # nosemgrep
            assert out.count(f"{name} ") == int(names is None or name in names)
