# Workshop Payment Workflow Build-Session Plan — Refund

## Summary
Use one short build session to implement the refund workflow
(`POST /payments/{payment_id}/refund`) under the local quality gates: behavior tests first,
smallest implementation, full `make verify`, rule audit, then PR and Qodo review.

## Starting State
- Branch: create a feature branch off `main` (e.g. `feat/payments-refund`).
- Current local verification: run `make doctor` then `make verify` on the clean starter; both should pass before changes.
- Selected repo-local rule IDs: `PAY-001`, `PAY-002`, `PAY-003`, `PAY-004`, `PAY-005`, `PAY-006`, `PAY-007`, `PAY-009`, `PAY-010`.
- Optional Qodo rules status: **not loaded** (`qodo-get-rules` unavailable; official Qodo skills not installed). Repo-local rules are the source of truth.

## Implementation Skill Handoff
- Planning skill completed: `workshop-plan-from-task`
- First implementation skill to run: `workshop-tdd-bdd`
- Required implementation prompt:
  ```text
  Use the workshop TDD/BDD skill and the refund plan in
  .plan/workshop-payment-task/. Write the smallest failing tests first for
  POST /payments/{payment_id}/refund: happy-path idempotent refund (capture
  pay_1001 first), missing Idempotency-Key -> 400, missing payments:refund
  scope -> 403 with no event, and refunding a non-captured payment -> 409 with
  no event. Put the idempotency replay check before the captured-state guard so
  a retried completed refund returns the original response. Do not write
  production code until the failing tests prove the behavior gap.
  ```
- Conditional skills to keep active during implementation:
  - `payment-idempotency` for idempotency keys, auth scope checks, event contract shape, and retry behavior.
  - `workshop-failure-path-testing` for the missing-key (400), missing-scope (403), and uncaptured-payment (409) gates.
- Review/remediation skills:
  - `workshop-guidelines-audit` before committing or opening the PR.
  - optional `workshop-pythonic-review` for changed Python code.
  - optional `qodo-pr-resolver` only after Qodo posts PR findings.

## Execution Steps
1. Run `make doctor`.
2. Run `make verify` on the clean starter to confirm a green baseline.
3. Read `AGENTS.md` and `rules/README.md`.
4. Confirm the selected `PAY-*` rule IDs for the refund path (see Starting State).
5. Optionally compare with Qodo rules if `qodo-get-rules` becomes available (currently not loaded).
6. Run the `workshop-tdd-bdd` prompt from the Implementation Skill Handoff.
7. Write failing tests in `tests/test_payments_api.py`: idempotent happy path (capture `pay_1001` first), `400` missing key, `403` missing scope (no event), `409` uncaptured (no event). Confirm they fail.
8. Implement `refund_payment` in `src/signalpay_api/app.py`, mirroring `capture_payment` (`app.py:93-125`) with the check order below. No `contracts.py` change.
9. Run targeted tests (`uv run pytest tests/test_payments_api.py -q`) until green.
10. Run `make verify`.
11. Run `workshop-guidelines-audit` against the diff.
12. Commit with Conventional Commits (`test(payments): ...`, then `feat(payments): ...`).
13. Push and open a PR.
14. Inspect Qodo findings on the PR.
15. Run PR Resolver or manually fix findings; do not weaken any gate (PAY-009).

### Refund handler check order (mirror of `capture_payment`)
1. `require_principal(authorization, required_scope="payments:refund")` — auth + scope before mutation (PAY-002).
2. Missing `Idempotency-Key` → `400` (PAY-001).
3. Unknown `payment_id` → `404`.
4. Idempotency replay: `result_key = ("refund", payment_id, idempotency_key)`; if cached, return it (PAY-003/004) — **before** the state guard.
5. State guard: if `status != "captured"` → `409` (PAY-010).
6. Mutate `status = "refunded"`; `build_payment_event(event_type="payment.refunded", ..., status="refunded")`; append `dict(event)`; cache `deepcopy(payment)`; return `Payment` with `response_model_by_alias=True` (PAY-005/006).

## Test Plan
- Targeted: `uv run pytest tests/test_payments_api.py -q` — new refund tests fail first, pass after implementation.
- Full: `make verify` — lint, typecheck, security, full pytest, semgrep all green.
- Add: one idempotent success-path test, one `400` missing-key test, one `403` missing-scope test, one `409` uncaptured test.
- Keep existing capture and contract tests passing.

## Risk Checks
- Idempotency: retried refund returns the original response; exactly one `payment.refunded` event per key (PAY-003/004).
- Auth scope: no state mutation or event before the `payments:refund` scope check (PAY-002).
- Event contract: event type is `payment.refunded`; event keys unchanged; built via `build_payment_event` (PAY-006).
- State transition: only `captured` payments refund; non-captured → `409`; replay check precedes the guard (PAY-010).
- Static analysis: Semgrep and Bandit clean; no committed secrets (PAY-008/009).

## Completion Notes
- Local verification:
- Repo rules applied:
- Qodo review:
- Remediation:
