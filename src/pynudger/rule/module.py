# SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Rules validating Python module."""

from __future__ import annotations

import itertools
import typing

import lintkit

from pynudger.rule import _code

if typing.TYPE_CHECKING:
    import ast
    import collections.abc


class Lines(
    lintkit.check.Check,
    lintkit.loader.Python,
    lintkit.rule.Node,
    code=29,
):
    """Rule checking Python modules with too many code lines."""

    def values(self) -> collections.abc.Iterable[lintkit.Value[int]]:
        """Yield number of lines of Python module.

        Yields:
            Counted code lines for the loaded Python source file.

        """
        # enq: optional access fine as it is always initialised in lintkit
        yield lintkit.Value(len(self.content.splitlines()))  # pyright: ignore[reportOptionalMemberAccess]

    def check(self, value: lintkit.Value[int]) -> bool:
        """Report modules with too many lines.

        Args:
            value:
                Lines of the loaded module.

        Returns:
            True if the lines exceed configured maximum,
            False otherwise.

        """
        return value > self._max_module_lines()

    def _max_module_lines(self) -> int:
        """Return the configured maximum number of lines.

        Returns:
            The maximum number of lines allowed in a module.
        """
        return self.config.get("max_module_lines", 600)  # pyright: ignore[reportAttributeAccessIssue]

    def description(self) -> str:
        """Return rule description.

        Returns:
            Description of the rule.

        """
        return (
            "Avoid modules with more than "
            f"{self._max_module_lines()} lines. "
            "Split it into focused modules."
        )

    def message(self, value: lintkit.Value[int]) -> str:
        """Return a module code-line violation message.

        Args:
            value:
                Lines for the loaded module.

        Returns:
            Message describing the rule violation.

        """
        return (
            f"Module has {value} lines, "
            f"which exceeds the maximum of {self._max_module_lines()}."
        )


class CodeLines(
    lintkit.check.Check,
    lintkit.loader.Python,
    lintkit.rule.Node,
    code=30,
):
    """Rule checking Python modules with too many code lines."""

    def values(self) -> collections.abc.Iterable[lintkit.Value[int]]:
        """Yield a single counted code-line value for a Python module.

        Yields:
            Counted code lines for the loaded Python source file.

        """
        # enq: optional access fine as it is always initialised in lintkit
        split = self.content.splitlines()  # pyright: ignore[reportOptionalMemberAccess]
        tree: ast.Module = self.getitem("ast")
        nodes_map: dict[type[ast.AST], list[ast.AST]] = self.getitem(
            "nodes_map"
        )
        docstring_nodes = itertools.chain.from_iterable(
            nodes_map[node_type]
            for node_type in typing.get_args(_code.Node.__value__)
        )
        yield lintkit.Value(_code.lines(tree, split, docstring_nodes))

    def check(self, value: lintkit.Value[int]) -> bool:
        """Report modules with too many counted code lines.

        Args:
            value:
                Counted code lines for the loaded module.

        Returns:
            True if counted code lines exceed configured maximum,
            False otherwise.

        """
        return value > self._max_module_code_lines()

    def _max_module_code_lines(self) -> int:
        """Return the configured maximum number of code lines.

        Returns:
            The maximum number of code lines allowed in a module.
        """
        return self.config.get("max_module_code_lines", 200)  # pyright: ignore[reportAttributeAccessIssue]

    def description(self) -> str:
        """Return rule description.

        Returns:
            Description of the rule.

        """
        return (
            "Avoid modules with more than "
            f"{self._max_module_code_lines()} code lines. "
            "Split code into focused modules."
        )

    def message(self, value: lintkit.Value[int]) -> str:
        """Return a module code-line violation message.

        Args:
            value:
                Counted code lines for the loaded module.

        Returns:
            Message describing the rule violation.

        """
        return (
            f"Module has {value} code lines, "
            f"which exceeds the maximum of {self._max_module_code_lines()}."
        )
