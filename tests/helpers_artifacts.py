import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict


def artifacts_dir(run_id: str) -> Path:
    base = Path(os.getenv("PYATTACKFORGE_ARTIFACT_DIR", ".codex/artifacts"))
    d = base / run_id
    d.mkdir(parents=True, exist_ok=True)
    return d


def report_path(run_id: str) -> Path:
    return artifacts_dir(run_id) / "report.json"


def _load_report(run_id: str) -> Dict[str, Any]:
    p = report_path(run_id)
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return {
        "run_id": run_id,
        "created_at": datetime.utcnow().isoformat() + "Z",
        "events": [],
    }


def write_event(run_id: str, test_name: str, event: Dict[str, Any]) -> None:
    data = _load_report(run_id)
    payload = {
        "ts": datetime.utcnow().isoformat() + "Z",
        "test": test_name,
        **event,
    }
    data["events"].append(payload)
    report_path(run_id).write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
