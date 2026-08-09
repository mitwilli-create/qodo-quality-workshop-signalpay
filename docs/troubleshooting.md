# Troubleshooting

## `make doctor` fails

Paste the output into your coding agent and ask it to fix missing local dependencies.

## Hosted-review setup is unavailable

This is intentional. Do not generate an application programming interface (API)
key or connect a hosted reviewer.
Continue with repo-local rules, local review skills, and `make verify`.

## Local rules cannot load

Continue with repo-local rules, repo-local skills, and visible standards:

- `AGENTS.md`
- `rules/README.md`
- `skills/payment-idempotency/SKILL.md`
- `.plan/workshop-payment-task/plan.md`

Document the missing local rule or skill in your pull request and stop if a required gate
cannot be verified.

## Local review is unclear

Inspect the diff against the selected rules and run the local review skill again.
Do not wait for or trigger a hosted reviewer.

## Semgrep is slow or unavailable

Semgrep is an optional advanced gate. Run the rest of the ladder:

```bash
make lint
make typecheck
make security
make test
```

## FastAPI `/docs` does not load

Confirm the server is running:

```bash
make run
```

Open:

```text
http://127.0.0.1:8000/docs
```
