# 02. Local Review Skills

The former hosted-review credential and skill setup lesson is retired. Do not
generate, store, or request a provider application programming interface (API)
key for this workshop.

## Install the local skills

```bash
make install-skills
```

This copies the committed skills into `.agents/skills/` and `.claude/skills/`
so attendees and coding agents can inspect the exact procedures used by the
workshop.

## Use the local rules

Read `rules/README.md`, select the relevant `PAY-*` rules, and use the matching
repo-local skill. Local rules, tests, lint, type checks, static analysis,
security checks, and `make verify` are the complete baseline.

## Agent prompt

```text
Read AGENTS.md, rules/README.md, and the relevant repo-local skills.
Select the PAY-* rules that apply to this task.
Write behavior tests before production code.
Run make verify, inspect the diff with the local review skill, and report every
pass, failure, or skipped check. Do not install or invoke a hosted reviewer.
```
