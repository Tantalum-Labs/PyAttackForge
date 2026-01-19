# tests/conftest.py
import os
import time
import random
import string
import pytest

def _is_truthy(value: str) -> bool:
    return str(value or "").lower() in ("1", "true", "yes", "y")

def _rand(n=6):
    return "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(n))

@pytest.fixture(scope="session")
def run_id():
    return f"PYAF-CI-{time.strftime('%Y%m%d-%H%M%S')}-{_rand()}"

def pytest_addoption(parser):
    parser.addoption("--live", action="store_true", help="Run live SSAPI integration tests")

def pytest_configure(config):
    config.addinivalue_line("markers", "live: live AttackForge SSAPI tests")

@pytest.fixture(scope="session")
def live_enabled(pytestconfig):
    # Prefer env var gate, but allow --live as well
    return os.getenv("PYATTACKFORGE_LIVE") == "1" or pytestconfig.getoption("--live")

@pytest.fixture(scope="session")
def af_env(live_enabled):
    if not live_enabled:
        pytest.skip("Live tests disabled (set PYATTACKFORGE_LIVE=1 or use --live)")

    base = os.getenv("ATTACKFORGE_BASE_URL")
    key = os.getenv("ATTACKFORGE_SSAPI_KEY")
    project_id = os.getenv("ATTACKFORGE_PROJECT_ID")

    missing = [k for k, v in {
        "ATTACKFORGE_BASE_URL": base,
        "ATTACKFORGE_SSAPI_KEY": key,
        "ATTACKFORGE_PROJECT_ID": project_id,
    }.items() if not v]

    if missing:
        pytest.skip(f"Missing live env vars: {', '.join(missing)}")

    cleanup = _is_truthy(os.getenv("PYATTACKFORGE_CLEANUP", "1"))
    return {
        "base_url": base,
        "ssapi_key": key,
        "project_id": project_id,
        "cleanup": cleanup,
    }
