# Workshop Refund Workflow Plan

Status: implemented and merged in pull request 1 on 2026-08-09.

## Summary

Add `POST /payments/{payment_id}/refund` while preserving authentication,
idempotency, event shape, and explicit payment-state transitions.

## Governing Rules

- `PAY-001` through `PAY-007` for payment mutation safety and tests.
- `PAY-009` for the complete local verification ladder.
- `PAY-010` for the `captured` to `refunded` transition.
- Hosted review is skipped by policy. Qodo and Greptile must not be invoked.

## Behavior

- A captured payment can be refunded once and replayed with the same key.
- Missing credentials, scope, idempotency key, or valid prior state fail before
  mutation or event emission.
- A refunded payment cannot be captured again with a different key.

## Verification

- The recapture regression test was observed failing before the production fix.
- Ruff, Pyright, Bandit, 18 Pytest tests, and Semgrep passed locally.
- The two pre-existing review threads were resolved at exact head `21086f0`.
- Pull request 1 was squash-merged as `81224ef`.

Local rules, local skills, and local verification are the complete review path.
