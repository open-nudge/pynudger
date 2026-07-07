<!--
SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
SPDX-FileContributor: szymonmaszke <github@maszke.co>

SPDX-License-Identifier: Apache-2.0
-->

# Tests of pynudger

- `test_smoke.py` - generic
    [smoke tests](https://grafana.com/blog/2024/01/30/smoke-testing/)
    to check if the package is importable.
- `test_rule.py` - run E2E tests of the command-line interface by running
    the CLI.
    Two different variations - one testing violations, and one testing
    no accidental variations are introduced by the tests.
- `test_description.py` - smoke test running `pynudger rules` to see if
    all are present

Note:

- One violation per test means each violation is tested consciously and no
    accidental violations are introduced.

<!-- Describe your testing here -->
