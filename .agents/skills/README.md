# Workshop Skills

Skills are repeatable procedures for coding agents. They turn repo standards into a workflow the agent can follow.

In this workshop, rules answer **what must be true**. Skills answer **how the agent should work** to preserve that truth.

## Skill Map

| Skill | Process phase | Teaching value |
| --- | --- | --- |
| `workshop-plan-from-task` | Planning | Converts a vague task into selected rules, scenarios, verification gates, and a handoff to implementation. |
| `workshop-tdd-bdd` | Test-first implementation | Forces behavior to be described as Given/When/Then scenarios before production code changes. |
| `payment-idempotency` | Payment mutation work | Keeps idempotency, auth-before-mutation, stable event shape, and retry behavior in the agent's working context. |
| `workshop-failure-path-testing` | Negative-path coverage | Makes unsafe behavior fail closed and proves blocked paths do not mutate state or emit events. |
| `workshop-guidelines-audit` | Pre-commit and pre-pull-request review | Checks the current diff against `AGENTS.md`, repo-local rules, selected skills, and verification evidence. |
| `workshop-pythonic-review` | Python review | Reviews changed Python code for maintainability without duplicating Ruff's lint checks. |

## How Skills Fit the Quality Loop

```text
plan-from-task -> tdd-bdd -> payment-idempotency/failure-path-testing -> guidelines-audit -> local review -> local remediation
```

The repo-local skills are committed so attendees can inspect them and agents can
use them without a provider account. Qodo and all other hosted-review skill
installations are outside this workshop's policy.

## Review Evidence Boundary

Be precise when presenting results:

- It is always safe to say the repo contains local skills.
- It is safe to say the coding agent used a local skill when the agent invocation or notes show that usage.
- Report only local skill usage that is visible in the prompt, plan, command
  output, or review receipt.

This distinction matters because the workshop is teaching evidence-based quality, not just tool configuration.
