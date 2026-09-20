# SPDX-FileCopyrightText: © 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Test module assignment with declaration names and kinds."""

from __future__ import annotations

import dataclasses

import pytest

from pynudger import _cli  # noqa: F401  # pyright: ignore[reportUnusedImport]
from pynudger.rule._constant import Kind, Strategy
from pynudger.rule.assignment import _raw_candidates


@dataclasses.dataclass(frozen=True)
class Case:
    """Store variable names and their expected assignment results.

    Attributes:
        names: Variable names in input order.
        stems: Expected target module stems in input order.
        renamed: Expected proposed names in input order.
        minimum: Required group size.
        strategy: Exact or greedy assignment strategy.
    """

    names: tuple[str, ...]
    stems: tuple[str | None, ...]
    renamed: tuple[str | None, ...]
    minimum: int = 2
    strategy: Strategy = Strategy.EXACT


@pytest.mark.parametrize(
    "case",
    (
        pytest.param(
            Case(
                (
                    "bank_account",
                    "account_name",
                    "_calculate_account",
                    "dataset_name",
                ),
                ("account", "name", "account", "name"),
                ("bank", "account", "_calculate", "dataset"),
            ),
            id="two-groups",
        ),
        pytest.param(
            Case(
                (
                    "account_billing",
                    "billing_account",
                    "account_support",
                    "support_only",
                ),
                ("account", "account", "support", "support"),
                ("billing", "billing", "account", "only"),
            ),
            id="exact-overlap",
        ),
        pytest.param(
            Case(
                (
                    "account_billing",
                    "billing_account",
                    "account_support",
                    "support_only",
                ),
                ("account", "account", "account", None),
                ("billing", "billing", "support", None),
                strategy=Strategy.GREEDY,
            ),
            id="greedy-overlap",
        ),
        pytest.param(
            Case(
                ("_account_value", "_account_status"),
                ("_account", "_account"),
                ("value", "status"),
            ),
            id="private-tie-exact",
        ),
        pytest.param(
            Case(
                ("_account_value", "_account_status"),
                ("_account", "_account"),
                ("value", "status"),
                strategy=Strategy.GREEDY,
            ),
            id="private-tie-greedy",
        ),
        pytest.param(
            Case(
                ("account_value", "_account_status"),
                ("account", "account"),
                ("value", "_status"),
            ),
            id="mixed-privacy",
        ),
        pytest.param(
            Case(
                ("alpha_beta", "beta_alpha"),
                ("alpha", "alpha"),
                ("beta", "beta"),
            ),
            id="lexical-tie",
        ),
        pytest.param(
            Case(
                ("alpha_beta", "beta_alpha", "alpha_gamma", "gamma_alpha"),
                ("alpha", "alpha", "alpha", "alpha"),
                ("beta", "beta", "gamma", "gamma"),
            ),
            id="fewer-groups",
        ),
        pytest.param(
            Case(
                ("account_value", "account_status", "account_owner"),
                ("account", "account", "account"),
                ("value", "status", "owner"),
                minimum=3,
            ),
            id="minimum-met",
        ),
        pytest.param(
            Case(
                ("account_value", "account_status", "account_owner"),
                (None, None, None),
                (None, None, None),
                minimum=4,
            ),
            id="minimum-missed",
        ),
        pytest.param(
            Case(
                ("grouped_owner", "owner_grouped", "grouped_status"),
                ("owner", "owner", None),
                ("grouped", "grouped", None),
            ),
            id="source-excluded",
        ),
        pytest.param(
            Case(
                ("repeat_repeat_alpha", "repeat_repeat_beta"),
                ("repeat", "repeat"),
                ("alpha", "beta"),
            ),
            id="repeated-word",
        ),
        pytest.param(
            Case(
                (
                    "__account_value",
                    "__account_bank",
                    "account_report",
                    "account_status",
                ),
                (None, None, "account", "account"),
                (None, None, "report", "status"),
            ),
            id="double-underscore",
        ),
        pytest.param(
            Case(
                ("_solo", "_solo_other"),
                ("_solo", "_solo"),
                ("solo", "other"),
            ),
            id="private-single-word",
        ),
        pytest.param(
            Case(
                ("account_value", "account_value"),
                ("account", "account"),
                ("value", "value"),
            ),
            id="repeated-declaration",
        ),
    ),
)
def test_variables(case: Case) -> None:
    """Check each variable's name, label, target, and proposed name.

    Args:
        case: Variable names and expected results in input order.
    """
    candidates = _raw_candidates(
        tuple((name, Kind.VARIABLE) for name in case.names),
        "grouped",
        case.minimum,
        case.strategy,
    )
    assert tuple(
        (item.name, item.label, item.stem, item.renamed) if item else None
        for item in candidates
    ) == tuple(
        (name, "Variable", stem, renamed) if stem is not None else None
        for name, stem, renamed in zip(
            case.names, case.stems, case.renamed, strict=True
        )
    )


@pytest.mark.parametrize(
    ("entries", "stems", "renamed"),
    (
        pytest.param(
            (
                (Kind.CLASS, "PaymentDebitError"),
                (Kind.CLASS, "PaymentCreditError"),
            ),
            ("payment", "payment"),
            ("DebitError", "CreditError"),
            id="class-error-suffix",
        ),
        pytest.param(
            ((Kind.CLASS, "HTTPClient"), (Kind.CLASS, "HTTPServer")),
            ("http", "http"),
            ("Client", "Server"),
            id="class-acronym",
        ),
        pytest.param(
            (
                (Kind.CLASS, "AccountManager"),
                (Kind.VARIABLE, "account_value"),
                (Kind.FUNCTION, "build_account"),
            ),
            ("account", "account", "account"),
            ("Manager", "value", "build"),
            id="mixed-kinds",
        ),
        pytest.param(
            ((Kind.CLASS, "ErrorHandler"), (Kind.CLASS, "ErrorLogger")),
            ("error", "error"),
            ("Handler", "Logger"),
            id="interior-error-word",
        ),
        pytest.param(
            ((Kind.CLASS, "_AccountModel"), (Kind.CLASS, "AccountView")),
            ("account", "account"),
            ("_Model", "View"),
            id="private-class",
        ),
    ),
)
def test_kinds(
    entries: tuple[tuple[Kind, str], ...],
    stems: tuple[str, ...],
    renamed: tuple[str, ...],
) -> None:
    """Check grouping and renaming across declaration kinds.

    Args:
        entries: Declaration kinds and names in input order.
        stems: Expected target module stems in input order.
        renamed: Expected proposed names in input order.
    """
    candidates = _raw_candidates(
        tuple((name, kind) for kind, name in entries),
        "grouped",
        2,
        Strategy.EXACT,
    )
    assert tuple(
        (item.name, item.label, item.stem, item.renamed) if item else None
        for item in candidates
    ) == tuple(
        (name, kind.title(), stem, proposed)
        for (kind, name), stem, proposed in zip(
            entries, stems, renamed, strict=True
        )
    )
