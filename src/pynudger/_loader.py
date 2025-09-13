# SPDX-FileCopyrightText: © 2025 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Pynudger loaders."""

from __future__ import annotations

import abc
import ast
import typing

import lintkit

if typing.TYPE_CHECKING:
    from collections.abc import Iterable

# Shared functionality


class _Definition(lintkit.loader.Python, abc.ABC):
    """Base class for loading class and function definitions."""

    @abc.abstractmethod
    def ast_class(self) -> type[ast.ClassDef | ast.FunctionDef]:
        """Return the AST class to look for.

        Returns:
            AST class to look for

        """
        raise NotImplementedError

    def values(self) -> Iterable[lintkit.Value[str]]:
        """Yield all definitions of the specified AST class.

        Yields:
            All definitions of the specified AST class

        """
        data: dict[type[ast.AST], list[ast.AST]] = self.getitem("nodes_map")
        for node in data[self.ast_class()]:
            yield lintkit.Value.from_python(
                node.name,  # pyright: ignore[reportUnknownArgumentType, reportAttributeAccessIssue]
                node,
            )


# Concrete loaders


class Class(_Definition):
    """Loader for function definitions."""

    def ast_class(self) -> type[ast.ClassDef]:
        """Return the AST class to look for.

        Returns:
            Always ast.ClassDef

        """
        return ast.ClassDef


class Function(_Definition):
    """Loader for function definitions."""

    def ast_class(self) -> type[ast.FunctionDef]:
        """Return the AST class to look for.

        Returns:
            Always ast.FunctionDef

        """
        return ast.FunctionDef


class Path(lintkit.loader.File):
    """Loader for file paths."""

    def values(self) -> Iterable[lintkit.Value[str]]:
        """Yield the file path as a value.

        Yields:
            The file path as a value
        """
        # COE: lintkit framework assures self.file is not None at this point
        yield lintkit.Value(str(self.file.stem))  # pyright: ignore[reportOptionalMemberAccess]
