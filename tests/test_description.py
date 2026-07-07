# SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Smoke test rule descriptions."""

from __future__ import annotations

import typing

import lintkit

from pynudger import _cli


def test_rules(capsys: typing.Any) -> None:
    """Smoke test rules provide descriptions.

    Args:
        capsys:
            Pytest system capture fixture (used for stdout/stderr analysis).

    """
    try:
        _cli.main(args=["rules"])
    except SystemExit:
        out, _ = capsys.readouterr()
        for i in lintkit.registry.codes():
            rule = f"{lintkit.settings.name}{i} "
            # nosemgrep
            assert out.count(rule) == 1
