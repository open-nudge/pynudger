# SPDX-FileCopyrightText: © 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Test declarations that share one case-insensitive name word."""

from __future__ import annotations

account_value = 1
build_value = 1


class _AccountModel:  # noqa: PYNUDGER38
    """Define an internal class sharing the account word."""


_ = _AccountModel()


def build_account() -> None:
    """Define a function sharing the account word."""


class HTTPClient:
    """Define a client sharing the HTTP acronym."""


class HTTPServer:
    """Define a server sharing the HTTP acronym."""


class PaymentDebitError(Exception):
    """Define a payment debit error."""


class PaymentCreditError(Exception):
    """Define a payment credit error."""


def repeat_repeat_alpha() -> None:
    """Define the first function with a repeated word."""


def repeat_repeat_beta() -> None:
    """Define the second function with a repeated word."""


def _solo() -> None:  # noqa: PYNUDGER37
    """Define a private function with one name word."""


def _solo_other() -> None:  # noqa: PYNUDGER37
    """Define a private function with two name words."""


_ = (_solo, _solo_other)
