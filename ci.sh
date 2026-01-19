#!/usr/bin/env bash
set -euo pipefail

# PyAttackForge project CI using the shared CodexWork CI addon
# Shared addon path: /root/CodexWork/ci.sh (relative from this project: ../ci.sh)

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

CI_ADDON="../ci.sh"
if [[ -f "$CI_ADDON" ]] && head -n 1 "$CI_ADDON" | grep -q "^#!/"; then
  # shellcheck disable=SC1091
  source "$CI_ADDON"
else
  codex_ci_begin() { :; }
  codex_ci_set_reason() { :; }
  codex_ci_set_status() { :; }
  codex_ci_run() { eval "$1"; }
  codex_ci_end() { :; }
fi

codex_ci_begin
codex_ci_set_reason "PyAttackForge CI: venv + deps + compileall + pytest (optionally live)"

echo "==> PyAttackForge CI"

PYTHON_BIN="${PYTHON_BIN:-python3}"

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  codex_ci_set_status "error"
  codex_ci_set_reason "Python interpreter not found: ${PYTHON_BIN}"
  codex_ci_end 2 error
  exit 2
fi

# Optional: keep a dedicated CI venv local to repo
VENV_DIR="${VENV_DIR:-.venv-ci}"

# Create / recreate venv with system site packages enabled (matches your current behavior)
if [[ ! -d "$VENV_DIR" ]]; then
  echo "==> Creating venv: $VENV_DIR"
  codex_ci_run "$PYTHON_BIN -m venv --system-site-packages $VENV_DIR" || {
    codex_ci_set_status "fail"
    codex_ci_set_reason "Failed to create venv: $VENV_DIR"
    codex_ci_end 1 fail
    exit 1
  }
else
  if [[ -f "$VENV_DIR/pyvenv.cfg" ]] && ! grep -q "include-system-site-packages = true" "$VENV_DIR/pyvenv.cfg"; then
    echo "==> Recreating venv with system site packages: $VENV_DIR"
    rm -rf "$VENV_DIR"
    codex_ci_run "$PYTHON_BIN -m venv --system-site-packages $VENV_DIR" || {
      codex_ci_set_status "fail"
      codex_ci_set_reason "Failed to recreate venv: $VENV_DIR"
      codex_ci_end 1 fail
      exit 1
    }
  fi
fi

# Activate venv
# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

# Load project env (kept from your original)
# shellcheck disable=SC1091
source ./setupEnv.sh

# Improve pip resiliency (helps with intermittent network/DNS hiccups)
export PIP_DISABLE_PIP_VERSION_CHECK=1
export PIP_DEFAULT_TIMEOUT="${PIP_DEFAULT_TIMEOUT:-15}"
export PIP_RETRIES="${PIP_RETRIES:-2}"

echo "==> Upgrading pip (best-effort)"
set +e
codex_ci_run "python -m pip install -U pip wheel setuptools --retries ${PIP_RETRIES} --timeout ${PIP_DEFAULT_TIMEOUT} >/dev/null"
set -e

echo "==> Installing runtime deps (best-effort)"
set +e
codex_ci_run "python -m pip install -r requirements.txt --retries ${PIP_RETRIES} --timeout ${PIP_DEFAULT_TIMEOUT} >/dev/null"
set -e

echo "==> Installing test deps (best-effort)"
set +e
codex_ci_run "python -m pip install pytest --retries ${PIP_RETRIES} --timeout ${PIP_DEFAULT_TIMEOUT} >/dev/null"
set -e

# If your repo later adds a dev requirements file, prefer it when present
if [[ -f requirements-dev.txt ]]; then
  echo "==> Installing dev deps (best-effort)"
  set +e
  codex_ci_run "python -m pip install -r requirements-dev.txt --retries ${PIP_RETRIES} --timeout ${PIP_DEFAULT_TIMEOUT} >/dev/null"
  set -e
fi

echo "==> Syntax check (compileall)"
codex_ci_run "python -m compileall -q pyattackforge" || {
  codex_ci_set_status "fail"
  codex_ci_set_reason "compileall failed"
  codex_ci_end 1 fail
  exit 1
}

echo "==> Running unit tests (non-live)"
codex_ci_run "python -m pytest -q -m \"not live\"" || {
  codex_ci_set_status "fail"
  codex_ci_set_reason "pytest (non-live) failed"
  codex_ci_end 1 fail
  exit 1
}

if [[ "${PYATTACKFORGE_LIVE:-0}" == "1" ]]; then
  echo "==> Running LIVE SSAPI tests"
  : "${ATTACKFORGE_BASE_URL:?ATTACKFORGE_BASE_URL is required for live tests}"
  : "${ATTACKFORGE_SSAPI_KEY:?ATTACKFORGE_SSAPI_KEY is required for live tests}"
  : "${ATTACKFORGE_PROJECT_ID:?ATTACKFORGE_PROJECT_ID is required for live tests}"

  codex_ci_run "python -m pytest -q -m \"live\"" || {
    codex_ci_set_status "fail"
    codex_ci_set_reason "pytest (live) failed"
    codex_ci_end 1 fail
    exit 1
  }
else
  echo "==> PYATTACKFORGE_LIVE is not set to 1; skipping live tests"
fi

echo "==> PASS"
codex_ci_set_status "pass"
codex_ci_set_reason "PyAttackForge CI passed"
codex_ci_end 0 pass
exit 0
