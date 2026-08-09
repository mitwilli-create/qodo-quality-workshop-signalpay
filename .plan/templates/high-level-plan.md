# High-Level Plan Template

Use this template to explain the intended change before implementation. Each
section should connect the task to a quality concern, a test signal, or a review
signal.

## Summary
- What problem are we solving?
- What quality constraints matter?
- Teaching value: this prevents the agent from treating the task as just a file edit.

## Skill Routing
- Selected repo-local rules:
- Hosted review status: skipped by policy
- Planning skill used: `workshop-plan-from-task`
- Implementation entry skill: `workshop-tdd-bdd`
- Conditional implementation skills:
  - `payment-idempotency` when changing payment mutation workflows.
  - `workshop-failure-path-testing` when adding or changing failure gates.
- Before-pull-request review skills:
  - `workshop-guidelines-audit`
  - optional `workshop-pythonic-review` for changed Python code
- Post-review workflow: address local review findings and verify again.
- Exact next prompt after planning:
  ```text
  Use the workshop test-driven development (TDD) and behavior-driven development (BDD) skill and the plan files just created.
  Write the smallest failing tests first for the selected behavior.
  Do not implement production code until the failing tests prove the behavior gap.
  ```
- Local verification gates:
- Teaching value: rules say what must stay true; skills tell the agent how to work; gates prove the result.

## Scope
- In:
- Out:
- Teaching value: scope keeps a workshop task small enough to verify and review.

## Behavior Scenarios
- Given ...
- When ...
- Then ...
- Teaching value: scenarios turn intent into observable behavior before production code changes.

## Verification Gates
- Tests:
- Lint:
- Typecheck:
- Security/static analysis:
- Repo rule audit:
- Local pull-request review:
- Teaching value: quality is checked early and often instead of waiting for the pull request.

## Failure and Recovery Rules
- What must fail closed?
- What error message should guide recovery?
- Teaching value: negative paths are where payment and auth bugs usually hide.

## Commit Plan
- `test(scope): ...`
- `feat(scope): ...`
- `docs(scope): ...`
- Teaching value: commits should preserve the story of tests, implementation, and docs.

## Definition of Done
- Local gates pass.
- Pull-request review is addressed.
- Human reviewer can understand the risk.
- Teaching value: done means verified and reviewable, not merely changed.

## Assumptions
- ...
- Teaching value: assumptions make hidden context explicit so reviewers can challenge it.
