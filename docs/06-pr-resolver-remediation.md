# 06. Local Review Remediation

Use the local review skill after the deterministic gates pass. This step
teaches that review feedback is part of the loop. The goal is to fix, defer
with rationale, and verify again.

## What the local review should do

- inspect the changed diff for correctness, security, quality, and contract
  violations
- preserve exact findings and severity
- apply fixes only after technical evaluation
- record deferred findings with a reason
- rerun `make verify`

## Checkpoint

You are done when:

- every finding is fixed or explicitly deferred with a reason
- proposed fixes have been reviewed before they are kept
- `make verify` passes again
- the pull request includes a short remediation summary

The human remains accountable for the code. Do not install or invoke Qodo,
Greptile, or another hosted reviewer to perform this step.
