import os
import random
import socket
import string
import time
from pathlib import Path
import json
from urllib.parse import urlparse
import pytest

from tests.helpers_artifacts import report_path


def _rand(n: int = 6) -> str:
    return "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(n))

def _parse_host(base_url: str) -> tuple[str, int]:
    base = (base_url or "").strip()
    if not base:
        return "", 443
    if "://" not in base:
        base = f"https://{base}"
    parsed = urlparse(base)
    host = parsed.hostname or ""
    if parsed.port:
        port = parsed.port
    elif parsed.scheme == "http":
        port = 80
    else:
        port = 443
    return host, port


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

    host, port = _parse_host(base)
    if host:
        try:
            socket.getaddrinfo(host, port)
        except socket.gaierror:
            pytest.skip(f"Unable to resolve ATTACKFORGE_BASE_URL host: {host}")

    return {"base_url": base, "ssapi_key": key, "project_id": project_id}


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    # Print artifact report location if it exists for this run.
    rid = None
    try:
        # Access fixture value indirectly via env if user wants; otherwise infer from report search
        rid = os.getenv("PYATTACKFORGE_LAST_RUN_ID")
    except Exception:
        rid = None

    # If env isn't set, try to locate a single report under artifact dir by mtime
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
            # quick counts
            uploaded = sum(1 for e in events if e.get("action") in ("upload_evidence", "upload_testcase_evidence") and e.get("uploaded") is True)
            skipped = sum(1 for e in events if e.get("reason") == "duplicate" or e.get("skipped") is True)
            terminalreporter.write_line(f"  uploaded: {uploaded}  skipped(dupe): {skipped}")
        except Exception:
            pass
