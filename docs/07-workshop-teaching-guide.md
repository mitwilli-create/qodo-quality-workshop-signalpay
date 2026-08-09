# 07. Workshop Teaching Guide

Use this guide when presenting the repo. The goal is to help attendees understand why each artifact exists, not only what command to run next.

## Teaching Frame

This repo demonstrates a quality-first artificial intelligence (AI) coding loop:

```text
task context -> plan -> repo rules -> repo skills -> tests -> implementation -> local gates -> pull request -> local review -> remediation
```

The lesson is that AI coding needs a control system around it. The coding agent can move quickly, but the repo gives it standards, tests, deterministic checks, and review feedback so speed does not turn into silent contract drift.

You can describe this as software development life cycle (SDLC) or artificial intelligence development life cycle (ADLC) quality control:

- **Before coding:** make intent, risk, and standards explicit.
- **During coding:** make behavior observable with tests and local static checks.
- **After coding:** use continuous integration (CI) and local review as an independent review layer.
- **After review:** remediate findings and rerun verification.

## Repository Tour

| Path | What it teaches |
| --- | --- |
| `README.md` | The workshop path, quality loop, hands-on task, and copy/paste prompts. |
| `AGENTS.md` | The agent operating contract: read rules, plan first, test first, verify, and do not weaken gates. |
| `.plan/` | Planning is a committed artifact in this workshop so attendees can inspect the reasoning before implementation. |
| `rules/` | Repo-local quality standards that humans and coding agents can inspect directly. |
| `skills/` | Repo-local agent procedures for planning, test-driven development (TDD), idempotency, failure-path testing, and review. |
| `docs/` | Step-by-step learning modules for local rules, gates, pull-request review, and remediation. |
| `src/signalpay_api/` | A deliberately small FastAPI payments application programming interface (API) with production-shaped risks. |
| `tests/` | Behavior tests that make payment safety requirements visible. |
| `.semgrep.yml` | Workshop-specific static analysis for payment idempotency risk. |
| `.github/workflows/verify.yml` | CI proof that the same local verification ladder runs on pull requests (PRs). |

The repo is small on purpose. The point is not payment-system completeness. The point is that each quality mechanism is visible enough to teach.

## Planning Layer

`.plan/` answers three questions before code changes start:

- What are we trying to change?
- Which quality constraints govern the change?
- Which tests and gates will prove the change is safe?

The high-level plan keeps the task tied to intent and risk. The build-session execution plan turns that intent into an ordered checklist that an agent can follow without inventing the workflow.

When presenting this section, emphasize that planning is not ceremony. It is how you keep an agent from optimizing only for "make the diff work" while missing auth, idempotency, event shape, or review evidence.

## Rules Layer

`rules/` contains the committed workshop standards. They are the default source of truth because every attendee and every coding agent can read them without portal setup.

Rules answer:

- What must never regress?
- Which tasks trigger which standards?
- What verification signal proves the rule was respected?

Hosted rules are outside this workshop. The repo-local Markdown rules keep the
lesson reliable without a provider account or portal setup.

## Skills Layer

`skills/` contains repeatable agent workflows. A rule says what standard matters. A skill tells the agent how to work under that standard.

For example, `payment-idempotency` turns an abstract payment safety concern into concrete checks:

- require `Idempotency-Key`
- check auth before mutation
- return the original response on retry
- avoid duplicate events
- test first request and retry behavior

Local review skills leverage the same team procedures during review. Report only
skill usage that is visible in the prompt, plan, command output, or receipt.

## Static Analysis and Gates

Local gates are deterministic checks that run before review:

| Gate | What it catches |
| --- | --- |
| Ruff | Python lint, imports, naming, and maintainability issues. |
| Pyright | Type and interface drift before runtime. |
| Bandit | Common Python security issues. |
| Pytest | Observable API behavior and payment safety expectations. |
| Semgrep | Workshop-specific patterns, such as idempotency bypasses. |
| Pre-commit | Formatting, security, and Conventional Commit checks at commit time. |
| CI | The same verification ladder on PRs. |

This is the early-and-often part of the lesson. Local review is valuable because
it adds context-aware review on top of these gates, not because it replaces them.

## Review and Remediation Layer

The PR is the independent review point. Attendees should inspect:

- bugs
- rule violations
- context used
- skill insights
- remediation guidance
- PR summary

Local remediation belongs after the local review skill has posted findings. It
helps apply or document fixes, but the human still reviews the changes and
reruns `make verify`.

## Presenter Script

Use this short explanation when you need to explain the repo quickly:

```text
This repo is built as a quality-control system for AI coding. The app is small, but the workflow is production-shaped. The agent starts with AGENTS.md, plans in .plan, reads repo-local PAY rules, uses repo-local skills, writes behavior tests, runs deterministic gates, performs a local review, opens a PR, then remediates findings and verifies again.

The important idea is that standards are useful at more than one point. We use them before coding as context, during coding as tests and static checks, and after coding as review criteria. This repo keeps the baseline committed in Markdown so every attendee can inspect and reuse it.
```

## What Good Looks Like

A successful attendee does not only produce a working diff. They produce a small PR with:

- selected `PAY-*` rules
- a plan and execution path
- behavior tests
- passing local gates
- PR review evidence
- remediation notes

That is the difference between "the agent changed files" and "the agent worked inside a quality system."
