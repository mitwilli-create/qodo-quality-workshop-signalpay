# 05. Open a Pull Request After Local Quality Assurance

Once local gates and the local review skill pass, open a pull request. Hosted
review is not automatic or required for this workshop.

## Commands

```bash
git checkout -b feat/payment-workflow
git add .
git commit -m "feat(payments): add refund workflow"
git push -u origin feat/payment-workflow
gh pr create --fill
```

## Checkpoint

You are ready when:

- the branch is pushed to your fork
- the pull request is open against the workshop repository
- local verification has passed
- the pull request describes the selected `PAY-*` rules and exact commands
- local review findings are fixed or documented with a reason

No hosted reviewer may be triggered from this lesson, a pull request comment, a
continuous-integration job, or an unattended loop.
