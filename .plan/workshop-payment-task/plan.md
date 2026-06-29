# Workshop Payment Workflow Plan — Refund

## Summary
Add a refund workflow (`POST /payments/{payment_id}/refund`) to the SignalPay API while
preserving the system's payment-safety guarantees: idempotency, auth scope checks, the
event contract shape, and one durable outcome per retry key.

This is a workshop task. The goal is to practice the quality workflow — read rules, plan,
write behavior tests first, run deterministic gates, review — more than to expand product
scope. The refund path is chosen because the contract layer is already pre-seeded for it
(`"refunded"` status, `"payment.refunded"` event type, and the `sp_live_payments_refund`
token all exist), so the change reuses existing symbols rather than inventing new ones.

Teaching value: this prevents the agent from treating the task as "just add an endpoint."
Refund is a payment mutation, so it must inherit every guarantee `capture` already enforces,
plus an explicit new state transition.

## Skill Routing
- Selected repo-local rules: `PAY-001`, `PAY-002`, `PAY-003`, `PAY-004`, `PAY-005`, `PAY-006`, `PAY-007`, `PAY-009`, `PAY-010`
- Optional Qodo rules: **not loaded** — official Qodo skills are not installed and no
  `qodo-get-rules` command is available. Repo-local `rules/` are the source of truth; do not
  block planning on portal setup. Compare with `qodo-get-rules` only if it becomes available.
- Planning skill used: `workshop-plan-from-task`
- Implementation entry skill: `workshop-tdd-bdd`
- Conditional implementation skills:
  - `payment-idempotency` because refund is a payment mutation path (idempotency key, auth scope, event contract, one-outcome-per-key).
  - `workshop-failure-path-testing` because missing key (400), missing scope (403), and uncaptured-payment (409) must fail closed.
- Pre-PR review skills:
  - `workshop-guidelines-audit`
  - optional `workshop-pythonic-review` for changed Python code
- Post-review skill: optional `qodo-pr-resolver` after Qodo posts PR findings.
- Exact next prompt after planning:
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
- Local verification gates: `make test`, `make lint`, `make typecheck`, `make security`, `make semgrep`, `make verify`

## Selected Repo Rules
- `PAY-001` — refund is a payment mutation, so it must reject requests with no `Idempotency-Key` (400) before any state change.
- `PAY-002` — validate the bearer token and the `payments:refund` scope before mutating state or emitting an event.
- `PAY-003` — key cached results by `("refund", payment_id, idempotency_key)` so a refund cannot replay a capture's result.
- `PAY-004` — a retried refund with the same key returns the original response and emits no second event.
- `PAY-005` — the refund response keeps stable camelCase fields (`paymentId`, `customerId`) via `response_model_by_alias=True`.
- `PAY-006` — emit the refund event through `build_payment_event` with type `payment.refunded`, preserving the stable event keys.
- `PAY-007` — write success and failure-path tests before the implementation.
- `PAY-009` — make all gates pass without weakening Ruff, Pyright, Bandit, Pytest, Semgrep, or pre-commit.
- `PAY-010` — the new `captured → refunded` transition is explicit and guarded; refunding a non-captured payment is rejected (409) and tested.

## Optional Qodo Rule Status
- Loaded: no (`qodo-get-rules` not available; official Qodo skills not installed)
- Differences from repo rules: not assessed — repo-local rules are the authoritative source for this task.

## Scope
- In:
  - Add `POST /payments/{payment_id}/refund` in `src/signalpay_api/app.py`, mirroring `capture_payment`.
  - Behavior tests in `tests/test_payments_api.py` written before the implementation.
  - Run the local deterministic gates and open a PR for Qodo review.
- Out:
  - changes to `src/signalpay_api/contracts.py` (refund status, event type, and token already exist)
  - database persistence
  - frontend dashboard
  - external payment processor integration
  - Docker or deployment

## Behavior Scenarios
- Given a `captured` payment and a token with `payments:refund`, when refund runs with a new idempotency key, then the payment becomes `refunded` and exactly one `payment.refunded` event is emitted.
- Given the same idempotency key is retried, when refund runs again, then the original response is returned and no second event is emitted.
- Given a token without the `payments:refund` scope, when refund runs, then the API returns `403` and no state or event changes.
- Given a missing `Idempotency-Key`, when refund runs, then the API returns `400` before any mutation.
- Given a payment that is not `captured`, when refund runs (no prior refund cached), then the API returns `409` and no state or event changes.

## Rule-Driven Test Expectations
- `test_refund_requires_an_idempotency_key` → `400`, detail names the missing header (PAY-001).
- `test_refund_requires_refund_scope` → `403` with reader/capture token; assert `payment_events` empty and payment status unchanged (PAY-002).
- `test_refund_rejects_uncaptured_payment` → `409` on an authorized/pending payment; assert no event and status unchanged (PAY-010).
- `test_refund_is_idempotent_and_emits_one_event` → capture `pay_1001` first, then refund twice with one key; assert identical payloads, `status == "refunded"`, exactly one `payment.refunded` event (PAY-003/004/006).
- Refund response payload asserts exact camelCase fields (PAY-005).

## Verification Gates
- `make test`
- `make lint`
- `make typecheck`
- `make security`
- `make semgrep`
- `make verify`
- repo-local rules audit (`workshop-guidelines-audit`)
- Qodo PR review

## Failure and Recovery Rules
- Fail closed before mutation: missing key → `400`, missing/invalid auth → `401`, missing scope → `403`, non-captured payment → `409`. None of these mutate state or emit events.
- **Replay-before-guard rule:** the idempotency replay check must run *before* the `captured`-state guard. Otherwise a legitimate retry of an already-completed refund sees `status == "refunded"` and is wrongly rejected with `409`. Replay-before-guard preserves PAY-004.
- Recovery messages should guide the caller: name the missing header, the required scope, or the required prior state.

## Commit Plan
- `test(payments): add failing refund behavior tests`
- `feat(payments): add idempotent refund endpoint`
- `docs(workshop): record refund verification evidence and rule audit`

## Definition of Done
- Behavior tests cover success and the 400 / 403 / 409 failure paths and fail before implementation.
- Local gates pass (`make verify`) with no weakened gates.
- Qodo findings are fixed or explicitly deferred with rationale.
- The PR explains the verification evidence and the selected repo rules.

## Assumptions
- In-memory state (`payments`, `payment_events`, `idempotency_results`) is the persistence model for the workshop; `reset_state()` isolates tests.
- "Refundable" means `status == "captured"`; the happy-path test reaches that state by calling the existing capture endpoint first.
- Refund amount equals the full payment amount (no partial refunds in this workshop scope).
