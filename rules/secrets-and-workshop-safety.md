# Secrets and Workshop Safety Rules

Use these rules when configuring agent skills, local environments, or setup docs.

## PAY-008: Hosted-review credentials and local secrets must never be committed

- Trigger: editing setup, local-agent, or credential-related files.
- Required behavior: do not create hosted-review credentials for this workshop.
  Never commit keys, `.env` files, local config, or generated secret material.
- Verification signal: git diff contains no application programming interface
  (API) keys, `.env` remains ignored,
  and setup docs tell participants how to store keys safely.

## Workshop Safety Notes

- Do not put local secrets under `rules/`.
- Do not create a hosted-review configuration directory.
- The committed repo-local rules are the complete source of truth for this
  workshop.
