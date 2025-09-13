# SPDX-FileCopyrightText: © 2025 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Pynudger rules."""

from __future__ import annotations

import lintkit

from pynudger._check import Common, Get, Helper, Pascal, Set, Snake, Util
from pynudger._loader import Class, Function, Path


# Setters rules
class SetClass(Set, Class, lintkit.rule.Node, code=0):
    """Rule checking class names for setters."""

    def description(self) -> str:
        """Return rule description."""
        return "Avoid using setters in class names. Use properties instead."


class SetFunction(Set, Function, lintkit.rule.Node, code=1):
    """Rule checking function names for setters."""

    def description(self) -> str:
        """Return rule description."""
        return "Avoid using setters in function names. Use properties instead."


class SetPath(Set, Path, lintkit.rule.Node, code=2):
    """Rule checking paths for setters."""

    def description(self) -> str:
        """Return rule description."""
        return "Avoid using setters in file names. Define file name without it."


# Getters rules
class GetClass(Get, Class, lintkit.rule.Node, code=3):
    """Rule checking class names for getters."""

    def description(self) -> str:
        """Return rule description."""
        return "Avoid using getters in class names. Use properties instead."


class GetFunction(Get, Function, lintkit.rule.Node, code=4):
    """Rule checking function names for getters."""

    def description(self) -> str:
        """Return rule description."""
        return "Avoid using getters in function names. Use properties instead."


class GetPath(Get, Path, lintkit.rule.Node, code=5):
    """Rule checking paths for getters."""

    def description(self) -> str:
        """Return rule description."""
        return "Avoid using getters in file names. Define file name without it."


# Util rules
class UtilClass(Util, Class, lintkit.rule.Node, code=6):
    """Rule checking class names for utils."""

    def description(self) -> str:
        """Return rule description."""
        return "Avoid using utils in class names. Name the class appropriately."


class UtilFunction(Util, Function, lintkit.rule.Node, code=7):
    """Rule checking function names for utils."""

    def description(self) -> str:
        """Return rule description."""
        return "Avoid using utils in function names. Name the function appropriately."


class UtilPath(Util, Path, lintkit.rule.Node, code=8):
    """Rule checking paths for utils."""

    def description(self) -> str:
        """Return rule description."""
        return "Avoid defining utils modules. Move functionality to appropriate modules."


# Helper rules
class HelperClass(Helper, Class, lintkit.rule.Node, code=9):
    """Rule checking class names for helpers."""

    def description(self) -> str:
        """Return rule description."""
        return (
            "Avoid using helpers in class names. Name the class appropriately."
        )


class HelperFunction(Helper, Function, lintkit.rule.Node, code=10):
    """Rule checking function names for helpers."""

    def description(self) -> str:
        """Return rule description."""
        return "Avoid using helpers in function names. Name the function appropriately."


class HelperPath(Helper, Path, lintkit.rule.Node, code=11):
    """Rule checking paths for utils."""

    def description(self) -> str:
        """Return rule description."""
        return "Avoid defining utils modules. Move functionality to appropriate modules."


# Common rules
class CommonClass(Common, Class, lintkit.rule.Node, code=12):
    """Rule checking class names for helpers."""

    def description(self) -> str:
        """Return rule description."""
        return (
            "Avoid using common in class names. Name the class appropriately."
        )


class CommonFunction(Common, Function, lintkit.rule.Node, code=13):
    """Rule checking function names for common."""

    def description(self) -> str:
        """Return rule description."""
        return "Avoid using common in function names. Name the function appropriately."


class CommonPath(Common, Path, lintkit.rule.Node, code=14):
    """Rule checking paths for commons."""

    def description(self) -> str:
        """Return rule description."""
        return "Avoid defining common modules. Move functionality to appropriate modules."


# Length rules
class LengthClass(Pascal, Class, lintkit.rule.Node, code=15):
    """Rule for checking class's name length (word-wise)."""

    def description(self) -> str:
        """Return rule description."""
        return "Avoid long class names. Specify intent by nesting modules/packages."


class LengthFunction(Snake, Function, lintkit.rule.Node, code=16):
    """Rule for checking function's name length (word-wise)."""

    def description(self) -> str:
        """Return rule description."""
        return "Avoid long function names. Specify intent by nesting modules/packages."


class LengthPath(Snake, Path, lintkit.rule.Node, code=17):
    """Rule for checking path name length (word-wise)."""

    def description(self) -> str:
        """Return rule description."""
        return (
            "Avoid long path names. Specify intent by nesting modules/packages."
        )
