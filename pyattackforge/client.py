"""High-level AttackForge client."""

from __future__ import annotations

from typing import Optional, Sequence, Dict, Any
import time

from .config import ClientConfig, config_from_env
from .exceptions import APIError
from .transport import AttackForgeTransport
from .resources import (
    AssetsResource,
    ProjectsResource,
    FindingsResource,
    WriteupsResource,
    TestcasesResource,
    TestsuitesResource,
    NotesResource,
    UsersResource,
    ReportsResource,
)


class AttackForgeClient:
    """Facade client exposing resource groups for the AttackForge SSAPI."""

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        config: Optional[ClientConfig] = None,
        timeout: Optional[float] = None,
        max_retries: Optional[int] = None,
        backoff_factor: Optional[float] = None,
        http2: Optional[bool] = None,
    ) -> None:
        if config is None:
            if base_url and api_key:
                config = ClientConfig(
                    base_url=base_url,
                    api_key=api_key,
                    timeout=30.0 if timeout is None else timeout,
                    max_retries=3 if max_retries is None else max_retries,
                    backoff_factor=0.5 if backoff_factor is None else backoff_factor,
                    http2=True if http2 is None else http2,
                )
            else:
                config = config_from_env()
        self._transport = AttackForgeTransport(config)

        self.assets = AssetsResource(self._transport)
        self.projects = ProjectsResource(self._transport)
        self.findings = FindingsResource(self._transport)
        self.writeups = WriteupsResource(self._transport)
        self.testcases = TestcasesResource(self._transport)
        self.testsuites = TestsuitesResource(self._transport)
        self.notes = NotesResource(self._transport)
        self.users = UsersResource(self._transport)
        self.reports = ReportsResource(self._transport)

    def close(self) -> None:
        self._transport.close()

    def __enter__(self) -> "AttackForgeClient":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def link_vulnerability_to_testcases(
        self,
        project_id: str,
        vulnerability_id: str,
        testcase_ids: Sequence[str],
        *,
        verify: bool = True,
        attempts: int = 3,
        delay: float = 1.0,
    ) -> Dict[str, Any]:
        """
        Link a vulnerability to project testcases, updating both sides (vulnerability + testcase).

        Best-effort: errors on either side do not raise by default. Returns linkage metadata.
        """
        candidates = [value for value in testcase_ids if value]
        if not candidates:
            return {"action": "noop", "linked_testcases": []}

        linked_testcases = set()
        try:
            vuln = self.findings.get_vulnerability(vulnerability_id)
            linked_testcases = self.findings.extract_linked_testcase_ids(vuln)
        except APIError:
            linked_testcases = set()

        updated = sorted(linked_testcases.union(candidates))
        if set(updated) != linked_testcases:
            payload = {"linked_testcases": updated, "projectId": project_id}
            try:
                self.findings.update_vulnerability(vulnerability_id, payload)
            except APIError:
                pass

        for testcase_id in candidates:
            try:
                testcases_data = self.testcases.get_project_testcases(project_id)
            except APIError:
                continue
            testcase = self.testcases.find_project_testcase_entry(testcases_data, testcase_id)
            if not testcase:
                continue
            existing = self.testcases.extract_linked_vulnerability_ids(testcase)
            if vulnerability_id in existing:
                continue
            payload = {"linked_vulnerabilities": sorted(existing.union({vulnerability_id}))}
            try:
                self.testcases.update_testcase(project_id, testcase_id, payload)
            except APIError:
                pass

        if not verify:
            return {"linked_testcases": updated, "verified": False}

        verified = False
        for _ in range(max(attempts, 1)):
            try:
                vuln = self.findings.get_vulnerability(vulnerability_id)
                linked_testcases = self.findings.extract_linked_testcase_ids(vuln)
            except APIError:
                linked_testcases = set()
            missing = [tc_id for tc_id in candidates if tc_id not in linked_testcases]
            if missing:
                time.sleep(delay)
                continue
            try:
                testcases_data = self.testcases.get_project_testcases(project_id)
            except APIError:
                time.sleep(delay)
                continue
            ok = True
            for tc_id in candidates:
                testcase = self.testcases.find_project_testcase_entry(testcases_data, tc_id)
                if not testcase:
                    ok = False
                    break
                linked_vulns = self.testcases.extract_linked_vulnerability_ids(testcase)
                if vulnerability_id not in linked_vulns:
                    ok = False
                    break
            if ok:
                verified = True
                break
            time.sleep(delay)
        return {"linked_testcases": updated, "verified": verified}
