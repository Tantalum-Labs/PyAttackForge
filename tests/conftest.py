import json
import os
import random
import socket
import string
import time
from pathlib import Path
from urllib.parse import urlparse

import pytest

from tests.helpers_artifacts import report_path


def _rand(n: int = 6) -> str:
    return "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(n))


@pytest.fixture(scope="session")
def run_id() -> str:
    return f"PYAF-CI-{time.strftime('%Y%m%d_%H%M%S')}-{_rand()}"


def pytest_addoption(parser):
    parser.addoption("--live", action="store_true", help="Run live SSAPI integration tests")


def pytest_configure(config):
    config.addinivalue_line("markers", "live: live AttackForge SSAPI tests")


@pytest.fixture(scope="session")
def live_enabled(pytestconfig) -> bool:
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

    parsed = urlparse(base if "://" in base else f"https://{base}")
    host = parsed.hostname
    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    if not host:
        pytest.skip("Invalid ATTACKFORGE_BASE_URL (missing hostname)")
    try:
        socket.create_connection((host, port), timeout=3).close()
    except OSError as exc:
        pytest.skip(f"Network error contacting SSAPI host {host}:{port}: {exc}")

    return {"base_url": base, "ssapi_key": key, "project_id": project_id}


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    # Only print the report path during the LIVE run invocation.
    markexpr = (getattr(getattr(config, "option", None), "markexpr", "") or "").strip()
    if "live" not in markexpr or "not live" in markexpr:
        return

    base = Path(os.getenv("PYATTACKFORGE_ARTIFACT_DIR", ".codex/artifacts"))
    report = None
    if base.exists():
        reports = list(base.glob("*/report.json"))
        if reports:
            report = max(reports, key=lambda p: p.stat().st_mtime)

    if report and report.exists():
        terminalreporter.write_line("")
        terminalreporter.write_line(f"PyAttackForge live run report: {report}")
        try:
            data = json.loads(report.read_text(encoding="utf-8"))
            events = data.get("events", [])
            terminalreporter.write_line(f"  events: {len(events)}")
            uploaded = sum(1 for e in events if e.get("action") in ("finding_evidence_upload", "testcase_file_upload") and e.get("uploaded") is True)
            skipped = sum(1 for e in events if e.get("reason") == "duplicate" or e.get("skipped") is True)
            terminalreporter.write_line(f"  uploaded: {uploaded}  skipped(dupe): {skipped}")
        except Exception:
            pass
