"""Resource: testsuites."""

from __future__ import annotations

from typing import Any, Dict, Optional, List
import os

from .base import BaseResource


class TestsuitesResource(BaseResource):
    """Testsuites API resource wrapper."""
    __test__ = False

    def create_testsuite(self, payload: Dict[str, Any]) -> Any:
        return self._post("/api/ss/testsuite", json=payload)

    def get_testsuites(self, params: Optional[Dict[str, Any]] = None) -> Any:
        return self._get("/api/ss/testsuites", params=params)

    def get_testsuite(self, testsuite_id: str) -> Any:
        return self._get(f"/api/ss/testsuites/{testsuite_id}")

    def update_testsuite(self, testsuite_id: str, payload: Dict[str, Any]) -> Any:
        return self._put(f"/api/ss/testsuite/{testsuite_id}", json=payload)

    def add_testcase_to_testsuite(self, testsuite_id: str, payload: Dict[str, Any]) -> Any:
        return self._post(f"/api/ss/testsuite/{testsuite_id}/testcase", json=payload)

    def add_testcases_to_testsuite(self, testsuite_id: str, payload: Dict[str, Any]) -> Any:
        return self._post(f"/api/ss/testsuite/{testsuite_id}/testcases", json=payload)

    def update_testcase_on_testsuite(self, testsuite_id: str, testcase_id: str, payload: Dict[str, Any]) -> Any:
        return self._put(f"/api/ss/testsuite/{testsuite_id}/testcase/{testcase_id}", json=payload)

    def upload_testsuite_testcase_file(self, testsuite_id: str, testcase_id: str, file_path: str) -> Any:
        if not os.path.isfile(file_path):
            raise FileNotFoundError(file_path)
        with open(file_path, "rb") as handle:
            return self._post_files(
                f"/api/ss/testsuites/{testsuite_id}/testcase/{testcase_id}/file",
                files={"file": (os.path.basename(file_path), handle)},
            )

    def download_testsuite_testcase_file(self, testsuite_id: str, testcase_id: str, file_name: str) -> Any:
        return self._get(f"/api/ss/testsuites/{testsuite_id}/testcase/{testcase_id}/file/{file_name}")

    def extract_testsuites_list(self, testsuites_data: Any) -> List[Dict[str, Any]]:
        if isinstance(testsuites_data, dict):
            testsuites = (
                testsuites_data.get("testsuites")
                or testsuites_data.get("data")
                or testsuites_data.get("testsuite")
            )
        else:
            testsuites = testsuites_data
        if not isinstance(testsuites, list):
            return []
        return [suite for suite in testsuites if isinstance(suite, dict)]

    def find_testsuite_by_name(
        self, name: str, *, testsuites_data: Optional[Any] = None, case_insensitive: bool = True
    ) -> Optional[Dict[str, Any]]:
        data = testsuites_data if testsuites_data is not None else self.get_testsuites()
        desired = self._normalize_string(name) if case_insensitive else name
        for suite in self.extract_testsuites_list(data):
            suite_name = suite.get("name")
            if not isinstance(suite_name, str):
                continue
            candidate = self._normalize_string(suite_name) if case_insensitive else suite_name
            if candidate == desired:
                return suite
        return None

    def extract_testsuite_testcases(self, suite_data: Any) -> List[Dict[str, Any]]:
        if isinstance(suite_data, dict):
            suite = suite_data.get("testsuite") if isinstance(suite_data.get("testsuite"), dict) else suite_data
            testcases = suite.get("testcases") if isinstance(suite, dict) else None
            if isinstance(testcases, list):
                return [tc for tc in testcases if isinstance(tc, dict)]
        return []

    def get_testsuite_testcases(self, testsuite_id: str) -> List[Dict[str, Any]]:
        data = self.get_testsuite(testsuite_id)
        return self.extract_testsuite_testcases(data)

    def _normalize_string(self, value: str) -> str:
        return value.strip().lower()
