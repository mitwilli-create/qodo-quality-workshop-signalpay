#!/usr/bin/env bash
set -euo pipefail

mkdir -p .agents/skills .claude/skills

for skill in skills/*; do
  [ -d "$skill" ] || continue
  name="$(basename "$skill")"
  mkdir -p ".agents/skills/$name" ".claude/skills/$name"
  cp -R "$skill"/. ".agents/skills/$name"/
  cp -R "$skill"/. ".claude/skills/$name"/
done

echo "Installed workshop skills into .agents/skills and .claude/skills."
echo "No hosted reviewer installation is required. Use the committed local skills."
