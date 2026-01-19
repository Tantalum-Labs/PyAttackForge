#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

echo "==> PyAttackForge CI"

PYTHON_BIN="${PYTHON_BIN:-python3}"

# Optional: keep a dedicated CI venv local to repo
VENV_DIR="${VENV_DIR:-.venv-ci}"

if [[ ! -d "$VENV_DIR" ]]; then
  echo "==> Creating venv: $VENV_DIR"
  "$PYTHON_BIN" -m venv --system-site-packages "$VENV_DIR"
else
  if [[ -f "$VENV_DIR/pyvenv.cfg" ]] && ! grep -q "include-system-site-packages = true" "$VENV_DIR/pyvenv.cfg"; then
    echo "==> Recreating venv with system site packages: $VENV_DIR"
    rm -rf "$VENV_DIR"
    "$PYTHON_BIN" -m venv --system-site-packages "$VENV_DIR"
  fi
fi

# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

source ./setupEnv.sh

echo "==> Upgrading pip"
if ! python -m pip install -U pip wheel setuptools >/dev/null; then
  echo "==> WARNING: pip upgrade failed; continuing with existing tooling"
fi

echo "==> Installing runtime deps"
if ! python -m pip install -r requirements.txt >/dev/null; then
  echo "==> WARNING: runtime dependency install failed; continuing with system packages"
fi

echo "==> Installing test deps"
if ! python -m pip install pytest >/dev/null; then
  echo "==> WARNING: pytest install failed; continuing with system packages"
fi

# If your repo later adds a dev requirements file, prefer it when present
if [[ -f requirements-dev.txt ]]; then
  if ! python -m pip install -r requirements-dev.txt >/dev/null; then
    echo "==> WARNING: dev dependency install failed; continuing with system packages"
  fi
fi

echo "==> Syntax check (compileall)"
python -m compileall -q pyattackforge

echo "==> Running unit tests"
python -m pytest -q -m "not live"

if [[ "${PYATTACKFORGE_LIVE:-0}" == "1" ]]; then
  echo "==> Running LIVE SSAPI tests"
  : "${ATTACKFORGE_BASE_URL:?ATTACKFORGE_BASE_URL is required for live tests}"
  : "${ATTACKFORGE_SSAPI_KEY:?ATTACKFORGE_SSAPI_KEY is required for live tests}"
  : "${ATTACKFORGE_PROJECT_ID:?ATTACKFORGE_PROJECT_ID is required for live tests}"
  python -m pytest -q -m "live"
else
  echo "==> PYATTACKFORGE_LIVE is not set to 1; skipping live tests"
fi

echo "==> PASS"
