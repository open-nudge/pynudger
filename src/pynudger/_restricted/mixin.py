# SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Reusable restricted checks and loaders."""

from __future__ import annotations

import abc
import ast
import typing

import lintkit

from pynudger._restricted import naming

if typing.TYPE_CHECKING:
    from collections.abc import Iterable


class Check(lintkit.check.Check, abc.ABC):
    """Check values loaded only when a restricted construct was found."""

    def check(self, _: lintkit.Value[typing.Any]) -> bool:
        """Report every loaded value as a rule violation.

        Args:
            _:
                Loaded restricted construct.

        Returns:
            Always ``True`` because loaders yield violations only.

        """
        return True

    def message(self, value: lintkit.Value[str]) -> str:
        """Return a restricted construct violation message.

        Args:
            value:
                Restricted construct name.

        Returns:
            Message describing the restricted construct.

        """
        return f"Avoid restricted {self.topic()}: '{value}'."

    @abc.abstractmethod
    def topic(self) -> str:
        """Return the restricted construct group name.

        Returns:
            Human-readable group name.

        """
        raise NotImplementedError

    @abc.abstractmethod
    def keywords(self) -> tuple[str, ...]:
        """Return restricted keyword names.

        Returns:
            Restricted keyword names checked by the rule.

        """
        raise NotImplementedError


class RuntimeCall(lintkit.loader.Python, abc.ABC):
    """Load restricted runtime calls by direct syntactic name."""

    def values(self) -> Iterable[lintkit.Value[str]]:
        """Yield restricted runtime calls.

        Yields:
            Restricted runtime calls.

        """
        data: typing.Any = self.getitem("nodes_map")
        keywords = self.keywords()
        for node in data[ast.Call]:
            name = naming.call(node.func)
            if name in keywords:
                yield lintkit.Value.from_python(name, node.func)

    @abc.abstractmethod
    def keywords(self) -> tuple[str, ...]:
        """Return restricted call names.

        Returns:
            Restricted runtime call names.

        """
        raise NotImplementedError
