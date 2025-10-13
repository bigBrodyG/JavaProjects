#!/usr/bin/env bash
# Simple wrapper to auto-add Java projects
# Works in any shell (bash, zsh, fish, etc.)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

cd "$PROJECT_ROOT"
python3 .github/scripts/auto-add-project.py "$@"
