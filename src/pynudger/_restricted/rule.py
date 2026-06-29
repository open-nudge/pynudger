# SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Registered restricted construct rules."""

from __future__ import annotations

import ast
import typing

import lintkit

from pynudger._restricted.mixin import (
    Check,
    RuntimeCall,
)

from pynudger._restricted import naming

if typing.TYPE_CHECKING:
    from collections.abc import Iterable


class State(Check, lintkit.loader.Python, lintkit.rule.Node, code=18):
    """Rule checking restricted state management keywords."""

    def values(self) -> Iterable[lintkit.Value[str]]:
        """Yield restricted state management statements.

        Yields:
            Check state management statements.

        """
        data: dict[type[ast.AST], list[ast.AST]] = self.getitem("nodes_map")
        for node in data[ast.Delete]:
            yield lintkit.Value.from_python("del", node)
        for node in data[ast.Global]:
            yield lintkit.Value.from_python("global", node)
        for node in data[ast.Nonlocal]:
            yield lintkit.Value.from_python("nonlocal", node)
        for node in data[ast.Pass]:
            yield lintkit.Value.from_python("pass", node)

    def description(self) -> str:
        """Return rule description."""
        return "Avoid restricted state management keywords: del, global, nonlocal, pass."

    def topic(self) -> str:
        """Return rule topic."""
        return "state management keywords"

    def keywords(self) -> tuple[str, ...]:
        """Return restricted keywords."""
        return ("del", "global", "nonlocal", "pass")


class IterationKeyword(Check, lintkit.loader.Python, lintkit.rule.Node, code=19):
    """Rule checking restricted iteration keywords."""

    def values(self) -> Iterable[lintkit.Value[str]]:
        """Yield restricted iteration control statements.

        Yields:
            Restricted iteration control statements.

        """
        data: dict[type[ast.AST], list[ast.AST]] = self.getitem("nodes_map")
        for node in data[ast.Break]:
            yield lintkit.Value.from_python("break", node)
        for node in data[ast.Continue]:
            yield lintkit.Value.from_python("continue", node)

    def description(self) -> str:
        """Return rule description."""
        return "Avoid restricted iteration keywords: break, continue."

    def topic(self) -> str:
        """Return rule topic."""
        return "iteration keywords"

    def keywords(self) -> tuple[str, ...]:
        """Return restricted keywords."""
        return ("break", "continue")


class Compatibility(
    Check,
    lintkit.loader.Python,
    lintkit.rule.Node,
    code=20,
):
    """Rule checking restricted compatibility functionality."""

    def values(self) -> Iterable[lintkit.Value[str]]:
        """Yield compatibility calls and class bases.

        Yields:
            Restricted compatibility constructs.

        """
        data: typing.Any = self.getitem("nodes_map")
        keywords = self.keywords()
        for node in data[ast.Call]:
            name = naming.call(node.func)
            if name in keywords:
                yield lintkit.Value.from_python(name, node.func)
        for node in data[ast.ClassDef]:
            for base in node.bases:
                name = naming.plain(base)
                if name in keywords:
                    yield lintkit.Value.from_python(name, base)

    def description(self) -> str:
        """Return rule description."""
        return "Avoid restricted compatibility functionality: object, basestring, unicode, long."

    def topic(self) -> str:
        """Return rule topic."""
        return "compatibility functionality"

    def keywords(self) -> tuple[str, ...]:
        """Return restricted keywords."""
        return ("object", "basestring", "unicode", "long")


class InteractiveFunction(
    Check,
    RuntimeCall,
    lintkit.rule.Node,
    code=21,
):
    """Rule checking restricted utility and interactive functions."""

    def description(self) -> str:
        """Return rule description."""
        return "Avoid restricted utility/interactive functions: breakpoint, help, id."

    def topic(self) -> str:
        """Return rule topic."""
        return "utility/interactive functions"

    def keywords(self) -> tuple[str, ...]:
        """Return restricted keywords."""
        return ("breakpoint", "help", "id")


class CastingFunction(Check, RuntimeCall, lintkit.rule.Node, code=22):
    """Rule checking restricted explicit casting functionality."""

    def description(self) -> str:
        """Return rule description."""
        return "Avoid restricted explicit casting functionality: typing.cast, bool, float, int, str."

    def topic(self) -> str:
        """Return rule topic."""
        return "explicit casting functionality"

    def keywords(self) -> tuple[str, ...]:
        """Return restricted keywords."""
        return ("typing.cast", "bool", "float", "int", "str")


class InsecureFunction(Check, RuntimeCall, lintkit.rule.Node, code=23):
    """Rule checking restricted insecure builtin functions."""

    def description(self) -> str:
        """Return rule description."""
        return (
            "Avoid restricted insecure builtin functions: exec, eval, compile."
        )

    def topic(self) -> str:
        """Return rule topic."""
        return "insecure builtin functions"

    def keywords(self) -> tuple[str, ...]:
        """Return restricted keywords."""
        return ("exec", "eval", "compile")


class ExplicitIteration(Check, RuntimeCall, lintkit.rule.Node, code=24):
    """Rule checking restricted explicit iteration functions."""

    def description(self) -> str:
        """Return rule description."""
        return "Avoid restricted explicit iteration: iter, aiter, anext, next."

    def topic(self) -> str:
        """Return rule topic."""
        return "explicit iteration"

    def keywords(self) -> tuple[str, ...]:
        """Return restricted keywords."""
        return ("iter", "aiter", "anext", "next")


class AttributeManipulation(
    Check,
    lintkit.loader.Python,
    lintkit.rule.Node,
    code=25,
):
    """Rule checking restricted attribute manipulation functionality."""

    def decorator_values(
        self, node: ast.FunctionDef | ast.AsyncFunctionDef
    ) -> Iterable[lintkit.Value[str]]:
        """Yield restricted property decorators from a definition.

        Args:
            node:
                Function definition whose decorators should be checked.

        Yields:
            Restricted property decorator values.

        """
        for decorator in node.decorator_list:
            name = naming.decorator(decorator)
            if name == "property":
                yield lintkit.Value.from_python(name, decorator)

    def values(self) -> Iterable[lintkit.Value[str]]:
        """Yield restricted attribute manipulation constructs.

        Yields:
            Restricted attribute manipulation calls and decorators.

        """
        data: typing.Any = self.getitem("nodes_map")
        keywords = self.keywords()
        for node in data[ast.Call]:
            name = naming.call(node.func)
            if name in keywords:
                yield lintkit.Value.from_python(name, node.func)

        for node in data[ast.FunctionDef]:
            yield from self.decorator_values(node)
        for node in data[ast.AsyncFunctionDef]:
            yield from self.decorator_values(node)

    def description(self) -> str:
        """Return rule description."""
        return (
            "Avoid restricted attribute manipulation: delattr, getattr, hasattr, "
            "setattr, globals, locals, vars, dir, property."
        )

    def topic(self) -> str:
        """Return rule topic."""
        return "attribute manipulation"

    def keywords(self) -> tuple[str, ...]:
        """Return restricted keywords."""
        return (
            "delattr",
            "getattr",
            "hasattr",
            "setattr",
            "globals",
            "locals",
            "vars",
            "dir",
            "property",
        )


class Dunder(Check, lintkit.loader.Python, lintkit.rule.Node, code=26):
    """Rule checking restricted explicit dunder attribute access."""

    def values(self) -> Iterable[lintkit.Value[str]]:
        """Yield explicit dunder attribute access.

        Yields:
            Dunder attribute names.

        """
        data: typing.Any = self.getitem("nodes_map")
        for node in data[ast.Attribute]:
            if node.attr.startswith("__"):
                yield lintkit.Value.from_python(node.attr, node)

    def description(self) -> str:
        """Return rule description."""
        return "Avoid restricted explicit dunder access: attributes starting with __."

    def topic(self) -> str:
        """Return rule topic."""
        return "explicit dunder access"

    def keywords(self) -> tuple[str, ...]:
        """Return restricted keywords."""
        return ("__*",)
