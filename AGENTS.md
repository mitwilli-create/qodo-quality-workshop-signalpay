# Agent Instructions

This repo is a quality-first artificial intelligence coding workshop app. The former Qodo workflow is
retired. Treat this as an exercise in local-first quality assurance (QA).

## Core Workflow

Follow this loop for implementation tasks:

1. Read the task and relevant docs.
2. Read `rules/README.md` and select the repo-local rule IDs that apply.
3. Use `.plan/templates/` to create a high-level plan and execution plan.
4. Write behavior tests before production code when behavior changes.
5. Implement the smallest useful change.
6. Run `make verify`.
7. Do not weaken verification gates to make a change pass.
8. Open a pull request (PR) after local QA and local review skills pass. Hosted review is not
   automatic or required for merge.

Qodo is fully halted. Do not install, authenticate, connect, or invoke it.
Use the committed repo-local rules and review skills as the complete QA path.

## Quality Rules

- Preserve idempotency for payment mutation endpoints.
- Preserve the public application programming interface (API) contract shape: camelCase JSON fields and stable event keys.
- Keep authentication and scope checks before state mutation.
- Add or update tests for every behavior change.
- Keep secrets out of git. Never commit hosted-review credentials.
- Use Conventional Commits for commit messages.
- Keep `rules/` as committed Markdown. Do not create a hosted-review config for
  this workshop.

## Local Commands

- `make run`: start the FastAPI app.
- `make verify`: run lint, typecheck, static analysis, tests, and Semgrep.
- `make doctor`: diagnose local workshop setup.
