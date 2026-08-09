# 01. Local Quality Assurance and GitHub

The former hosted-review setup lesson is retired. Qodo is fully halted, the
account and integrations are deleted, and this workshop must not connect a
repository to Qodo or any other hosted reviewer.

## Current workflow

1. Read `AGENTS.md`, `rules/README.md`, and the applicable `PAY-*` rules.
2. Install the committed local skills with `make install-skills`.
3. Write behavior tests before implementation.
4. Run `make verify`, inspect the diff with the local review skill, and record
   the exact evidence.
5. Open a pull request only after local quality assurance passes.

No provider account, application programming interface (API) key, hosted dashboard, or automatic reviewer is
required. If an old copy of this lesson tells you to connect a provider, treat
that instruction as superseded.
