# Local Quality-First Artificial Intelligence Coding Workshop

This repo is the source of truth for a one-hour hands-on workshop on building a quality-first, local-first artificial intelligence (AI) coding workflow. The former Qodo workflow is retired.

You will practice this loop:

```text
plan -> read repo rules -> use repo skills -> write tests -> implement -> run local gates -> local review -> open pull request (PR) -> verify again
```

## What You Are Building

This is a self-contained FastAPI payments application programming interface (API) used to practice quality-first AI coding.

It has no separate frontend and no external service dependencies. You will interact with the app through FastAPI's browser docs at `/docs`.

The goal is not to build a production payment system. The goal is to practice a repeatable workflow:

```text
plan -> read repo rules -> write tests -> implement -> run local gates -> local review -> open pull request -> resolve findings
```

## What This Repo Is Teaching

This workshop is a small API wrapped in a quality system. Every directory is here to teach one part of quality-first AI coding:

- make the task explicit before code changes
- give the agent local standards it can read
- give the agent skills that describe how to work
- prove behavior with tests
- catch deterministic issues with static analysis and local gates
- use a local review skill as an independent review layer
- remediate findings and verify again

You can describe this as software development life cycle (SDLC) or artificial intelligence development life cycle (ADLC) quality control. The same standards show up before coding, during coding, and after coding:

| Phase | Repo artifact | Teaching point |
| --- | --- | --- |
| Before coding | `AGENTS.md`, `.plan/`, `rules/`, `skills/` | Agents need intent, standards, and procedures before they generate code. |
| During coding | `tests/`, `src/`, `.semgrep.yml`, `Makefile` | Behavior and static checks make quality observable while the change is still local. |
| After coding | `.github/workflows/verify.yml`, local review, pull request | Continuous integration (CI) and local review add independent evidence and remediation after local verification. |

Read the presenter-focused lesson in [docs/07-workshop-teaching-guide.md](docs/07-workshop-teaching-guide.md).

## Repository Structure

| Path | Purpose |
| --- | --- |
| `AGENTS.md` | Operating instructions for coding agents in this repo. |
| `.plan/` | Planning templates and example plans that explain intent, risk, rules, tests, and execution order. |
| `rules/` | Repo-local `PAY-*` quality rules that are always available to humans and agents. |
| `skills/` | Repo-local agent procedures for planning, test-driven development (TDD), payment idempotency, failure-path testing, and review. |
| `docs/` | Guided workshop lessons for local rules, gates, pull-request review, and remediation. |
| `src/signalpay_api/` | The small FastAPI payment API used for the hands-on task. |
| `tests/` | Behavior and structure tests that make the workshop contract visible. |
| `.semgrep.yml` | Workshop-specific static analysis for payment mutation risks. |
| `.github/workflows/verify.yml` | CI gate that reruns the local verification ladder on PRs. |

The app is intentionally small so the quality system is easy to inspect. The teaching point is the loop around the code, not the size of the feature.

## Workshop App

Run the app locally:

```bash
make setup
make run
```

Open:

```text
http://127.0.0.1:8000/docs
```

Also available:

```text
http://127.0.0.1:8000/redoc
http://127.0.0.1:8000/openapi.json
```

This workshop app is API-first. The browser user interface (UI) is FastAPI `/docs`, not a separate React dashboard.

## Choose Your Lane

- **Hands-on:** fork, clone, run local quality assurance (QA), make the change, open a pull request.
- **Pair/observe:** follow the README and inspect the gates while someone else codes.
- **Async later:** use this repo as a complete guided workshop after the session.

## One-Hour Flow

| Time | Activity |
| --- | --- |
| 0-5 min | Frame quality-first AI coding: deterministic gates + repo rules/skills + local review. |
| 5-10 min | Open this README, choose a lane, fork and clone. |
| 10-15 min | Run `make doctor`; let your coding agent troubleshoot setup. |
| 15-22 min | Read the repo-local rules and review skills. |
| 22-28 min | Create the plan and select the applicable quality rules. |
| 28-34 min | Use repo skills before coding and confirm the local QA command. |
| 34-43 min | Write behavior tests and implement the payment workflow change. |
| 43-50 min | Run lint, typecheck, static analysis, tests, and pre-commit. |
| 50-56 min | Commit, push, open PR, inspect local review evidence. |
| 56-60 min | Resolve findings and rerun the local verification ladder. |

## Quality Gate Checkpoints

Use these checkpoints to know what you have completed at each step. Each gate
should leave behind visible proof that the workflow is moving forward.

- **Setup gate:** `make doctor`, `make setup`, and starter `make verify` run
  successfully. You have a working local repo before asking an agent to change
  application behavior.
- **Review setup gate:** local review skills are installed, the local QA command
  is known, and no hosted-review credential or integration is required.
- **Standards gate:** the relevant `PAY-*` rules are selected, linked rule docs
  are read, and repo skills are identified. You have turned the task into
  explicit quality constraints.
- **Planning and TDD gate:** the high-level plan, build-session execution plan,
  and smallest useful failing behavior tests are identified or written. You
  have made the expected behavior observable before production code changes.
- **Local verification gate:** targeted tests and `make verify` pass without
  disabling Ruff, Pyright, Bandit, Pytest, Semgrep, or commit checks. You have
  deterministic evidence that the change preserves the local contract.
- **PR review and remediation gate:** the PR is open, local review findings are
  inspected, fixes or deferrals are documented, and `make verify` is rerun after
  remediation. You have completed the review loop rather than stopping at a
  passing local run.

## Prerequisites

Read [docs/00-prerequisites.md](docs/00-prerequisites.md).

Required:

- Git
- GitHub account
- GitHub CLI authenticated with `gh auth login`
- Python 3.11+
- `uv`
- Node.js and npm
- A coding agent such as Codex, Claude Code, Cursor, Windsurf, or Cline

## Setup

```bash
git clone <your-fork-url>
cd qodo-quality-workshop-signalpay
make doctor
make setup
make verify
```

If setup fails, paste the `make doctor` output into your coding agent and ask it to fix your local environment.

Install repo-local workshop skills:

```bash
make install-skills
```

## Repo-Local Rules

The default pre-coding context is committed in [rules/README.md](rules/README.md).
No hosted-review setup is required or permitted for this workshop.

Repo-local rules are intentionally Markdown. That makes them readable by:

- attendees
- coding agents
- reviewers
- local review skill inspection

In the workshop, local rules and skills are the complete baseline and review path.

## Repo-Local Skills

Repo-local skills are committed in [skills/](skills/). They teach the agent how to work inside the rules.

For example, the `payment-idempotency` skill translates payment safety into concrete implementation checks: require `Idempotency-Key`, check auth before mutation, return the original response on retry, and avoid duplicate events.

Use [skills/README.md](skills/README.md) to explain which skill belongs to each phase of the workflow.

## Hands-On Task: Payment Workflow Safety

Your task is to add one small payment workflow: either a refund workflow or capture-retry handling. Choose one path for the workshop; do not try to build both.

This is intentionally a small change with production-shaped risk. Payment mutations are where AI-generated code can look correct while quietly breaking system guarantees. A retry can emit a duplicate event, a missing idempotency key can create duplicate work, an auth check can happen after state changes, or a response can drift from the public API contract.

The point of this exercise is to practice making an agent work inside a quality system before it writes code. You will force the agent to read local rules, select the `PAY-*` standards that apply, use the payment-idempotency skill, write behavior tests first, run deterministic gates, and then inspect local review feedback.

By the end, you should be able to see the difference between "the agent changed files" and "the agent produced a change that preserved the system contract." The expected output is a small PR with tests, verification evidence, and a review/remediation loop, not a large feature.

Preserve these guarantees:

- idempotency
- auth scope checks
- event contract shape
- one-event-per-idempotency-key behavior

Use this task as the input for the setup, planning, TDD, and verification prompts below.

Read [docs/03-run-rules-before-coding.md](docs/03-run-rules-before-coding.md), then start from:

- [.plan/workshop-payment-task/plan.md](.plan/workshop-payment-task/plan.md)
- [.plan/workshop-payment-task/build-session-execution-plan.md](.plan/workshop-payment-task/build-session-execution-plan.md)

When presenting this step, point out that `.plan/` is part of the lesson. The high-level plan explains intent and quality constraints. The build-session execution plan turns those constraints into an ordered agent workflow.

## Definition of Done

The workshop task is complete when you have a small PR that includes:

- selected repo-local rules and local review skill status
- behavior tests and verification evidence
- a passing `make verify` run without weakened gates
- local review evidence and any documented skipped checks
- remediation notes for fixed or intentionally deferred findings

## Copy/Paste Agent Prompts

### Setup Prompt

```text
Help me configure this repo for the local-first quality workshop.

Requirements:
- Do not install or configure a hosted reviewer.
- Install or verify the repo-local review skills.
- Read `AGENTS.md` and `rules/README.md`.
- Select the relevant repo-local rule IDs for the Hands-On Task and explain why each applies.
- If my local environment is missing dependencies, diagnose and fix them.
```

### Planning Prompt

```text
Use the repo-local workshop planning skill to turn the Hands-On Task in README.md into:
1. a high-level implementation plan
2. a build-session execution plan

Use `AGENTS.md`, `rules/README.md`, selected `PAY-*` rules, and the
payment-idempotency skill as constraints.
The plan must include an implementation skill handoff that names the first
implementation skill and the exact TDD prompt to run next.
Do not invoke Qodo or install hosted-review skills. Local rules and skills are
the complete baseline.
Do not write code yet.
```

### TDD Prompt

Run this only after the planning prompt has produced the high-level plan,
build-session execution plan, and implementation skill handoff.

```text
Use the workshop TDD/BDD skill.

Use the plan files just created.
Write the smallest failing tests first for the selected payment workflow path.
Cover one happy path and at least one failure path.
Do not implement production code until the failing tests prove the behavior gap.
```

### Verification Prompt

```text
Run the full local verification ladder.

If anything fails, classify the failure as formatting, linting, type checking, security/static analysis, behavior, or repo guideline compliance.
Fix the issue without weakening the gate.
Re-run verification.
```

## Local Verification Gates

Run individual gates:

```bash
make lint
make typecheck
make security
make test
make semgrep
```

Run the full ladder:

```bash
make verify
```

Read [docs/04-local-verification-gates.md](docs/04-local-verification-gates.md).

These gates catch deterministic issues early:

- Ruff checks Python lint, imports, and maintainability.
- Pyright catches type and interface drift.
- Bandit checks common Python security risks.
- Pytest proves API behavior.
- Semgrep checks workshop-specific static-analysis patterns.
- CI reruns the same ladder on PRs.

Local review adds a second perspective after these gates; it does not replace them.

## Open a PR After Local QA

```bash
git checkout -b feat/payment-workflow
git add .
git commit -m "feat(payments): add refund workflow"
git push -u origin feat/payment-workflow
gh pr create --fill
```

Read:

- [docs/05-open-pr-and-qodo-review.md](docs/05-open-pr-and-qodo-review.md)
- [docs/06-pr-resolver-remediation.md](docs/06-pr-resolver-remediation.md)

In the local review, distinguish evidence from configuration. Report the exact
local commands, findings, fixes, and skipped checks. Do not claim hosted-review
coverage.

## Slides

The live companion deck is linked from [slides/README.md](slides/README.md).

## Fallbacks

- Local setup failing? Paste `make doctor` output into your coding agent.
- Hosted-review setup is intentionally unavailable. Continue with repo skills and local gates.
- Hosted review is unavailable by policy. Use local review skills and the
  prepared local evidence instead.
- Behind the room? Continue asynchronously from this README.
