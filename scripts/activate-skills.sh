#!/usr/bin/env bash
# Link project skills into ~/.cursor/skills for global discovery in this environment.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET="${HOME}/.cursor/skills"
SOURCE="${ROOT}/.cursor/skills"

if [[ ! -d "${SOURCE}" ]]; then
  echo "error: ${SOURCE} not found" >&2
  exit 1
fi

mkdir -p "${HOME}/.cursor"
if [[ -e "${TARGET}" && ! -L "${TARGET}" ]]; then
  echo "error: ${TARGET} exists and is not a symlink; remove or rename it first" >&2
  exit 1
fi

ln -sfn "${SOURCE}" "${TARGET}"
count="$(find "${SOURCE}" -name SKILL.md | wc -l | tr -d ' ')"
echo "Activated ${count} skills: ${TARGET} -> ${SOURCE}"
