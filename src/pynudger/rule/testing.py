# SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Rules validating test structure."""

from __future__ import annotations

import ast
import typing

import lintkit

if typing.TYPE_CHECKING:
    import collections.abc


class AssertCount(
    lintkit.check.Check,
    lintkit.loader.Python,
    lintkit.rule.Node,
    code=28,
):
    """Rule checking extra assert statements in pytest tests."""

    def values(self) -> collections.abc.Iterable[lintkit.Value[ast.Assert]]:
        """Yield assert statements from pytest-style functions.

        Yields:
            Assert statements inside matching test functions.

        """
        path = self.file.resolve()  # pyright: ignore[reportOptionalMemberAccess]
        if not path.name.startswith("test") and not path.stem.endswith("test"):
            return

        data: list[ast.FunctionDef] = self.getitem("nodes_map")[ast.FunctionDef]
        for function_def in data:
            if function_def.name.startswith("test"):
                self._count: int = 0
                for statement in function_def.body:
                    if isinstance(statement, ast.Assert):
                        yield lintkit.Value.from_python(statement, statement)
            else:  # pragma: no cover
                pass

    def check(self, _: lintkit.Value[ast.Assert]) -> bool:
        """Report asserts only when a test contains too many of them.

        Args:
            _:
                Loaded assert statement.

        Returns:
            True if the current test function has more than two asserts.

        """
        self._count += 1
        return self._count > self._maximum_test_asserts()

    def _maximum_test_asserts(self) -> int:
        """Get maximum number of allowed asserts in test cases.

        Returns:
            Maximum number of allowed asserts in test cases.
            Default: 1
        """
        return self.config.get("maximum_test_asserts", 1)  # pyright: ignore[reportAttributeAccessIssue]

    def description(self) -> str:
        """Return rule description.

        Returns:
            Description of the rule.

        """
        return (
            f"Avoid more than {self._maximum_test_asserts()} assert "
            "statements in pytest tests. Keep each test focused."
        )

    def message(self, _: lintkit.Value[ast.Assert]) -> str:
        """Return a multiple-assert violation message.

        Args:
            _:
                Extra assert statement.

        Returns:
            Message describing the rule violation.

        """
        return self.description()
