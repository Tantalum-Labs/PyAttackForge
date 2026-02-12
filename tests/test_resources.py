import os
import tempfile
from types import SimpleNamespace

from pyattackforge.resources import (
    AssetsResource,
    ProjectsResource,
    GroupsResource,
    FindingsResource,
    WriteupsResource,
    TestcasesResource,
    TestsuitesResource,
    NotesResource,
    UsersResource,
    ReportsResource,
)


class FakeTransport:
    def __init__(self):
        self.calls = []
        self.queue = []

    def enqueue(self, data):
        self.queue.append(data)

    def request(self, method, path, **kwargs):
        self.calls.append((method, path, kwargs))
        data = self.queue.pop(0) if self.queue else {"ok": True}
        return SimpleNamespace(status_code=200, data=data, headers={})


def test_assets_resource_calls():
    transport = FakeTransport()
    assets = AssetsResource(transport)
    assets.create_asset_in_library({"name": "a"})
    assets.update_asset_in_library("id1", {"name": "b"})
    assets.get_assets()
    assets.get_asset_in_library("id2")
    assets.get_asset_library_assets({"query": "x"})

    assert transport.calls[0][0] == "POST"
    assert transport.calls[0][1] == "/api/ss/library/asset"
    assert transport.calls[1][0] == "PUT"
    assert transport.calls[1][1] == "/api/ss/library/asset/id1"
    assert transport.calls[2][0] == "GET"
    assert transport.calls[2][1] == "/api/ss/assets"
    assert transport.calls[3][1] == "/api/ss/library/asset"
    assert transport.calls[3][2]["params"]["id"] == "id2"
    assert transport.calls[4][1] == "/api/ss/library/assets"


def test_projects_resource_calls():
    transport = FakeTransport()
    projects = ProjectsResource(transport)
    projects.create_project({"name": "p"})
    projects.get_project("p1")
    projects.get_projects()
    projects.get_projects_and_vulnerabilities()
    projects.update_project("p2", {"name": "u"})
    projects.archive_project("p3")
    projects.restore_project("p4")
    projects.destroy_projects(["p5"])
    projects.clone_project("p6")
    projects.create_scope("p7", {"assets": ["a"]})
    projects.update_scope("p8", "a1", {"asset": "x"})
    projects.get_project_workspace("p9")
    projects.download_workspace_file("p10", "file.txt")
    projects.get_project_notes("p11")
    projects.create_project_note("p12", {"note": "x"})
    projects.update_project_note("p13", "n1", {"note": "y"})
    projects.create_project_workspace_note("p14", {"note": "z"})
    projects.update_project_workspace_note("p15", "n2", {"note": "w"})
    projects.get_project_membership_administrators("p16")
    projects.add_project_membership_administrators("p17", {"user_ids": ["u1"]})
    projects.update_project_membership_administrators("p18", {"user_ids": ["u2"]})
    projects.remove_project_membership_administrators("p19", {"user_ids": ["u3"]})
    projects.invite_user_to_project("p20", {"username": "a"})
    projects.invite_users_to_project_team("p21", {"users": []})
    projects.remove_project_team_members("p22", {"users": []})
    projects.update_user_access_on_project("p23", "u4", {"update": "Edit"})

    assert transport.calls[0][1] == "/api/ss/project"
    assert transport.calls[1][1] == "/api/ss/project/p1"
    assert transport.calls[2][1] == "/api/ss/projects"
    assert transport.calls[3][1] == "/api/ss/projects-and-vulnerabilities"
    assert transport.calls[7][1] == "/api/ss/project/destroy"
    assert transport.calls[10][1] == "/api/ss/project/p8/asset/a1"
    assert transport.calls[11][1] == "/api/ss/project/p9/workspace"
    assert transport.calls[12][1] == "/api/ss/project/p10/workspace/file.txt"
    assert transport.calls[19][1] == "/api/ss/project/p17/member-admins"
    assert transport.calls[20][1] == "/api/ss/project/p18/member-admins"
    assert transport.calls[22][1] == "/api/ss/project/p20/invite"
    assert transport.calls[23][1] == "/api/ss/project/p21/team/invite"
    assert transport.calls[-1][1] == "/api/ss/project/p23/access/u4"


def test_projects_add_project_to_group():
    transport = FakeTransport()
    transport.enqueue({"project": {"groups": [{"id": "g1"}]}})
    projects = ProjectsResource(transport)
    projects.add_project_to_group("p1", "g2")

    assert transport.calls[0][0] == "GET"
    assert transport.calls[0][1] == "/api/ss/project/p1"
    assert transport.calls[1][0] == "PUT"
    assert transport.calls[1][1] == "/api/ss/project/p1"
    assert transport.calls[1][2]["json"]["groups"] == ["g1", "g2"]


def test_groups_resource_calls():
    transport = FakeTransport()
    groups = GroupsResource(transport)
    groups.get_groups()
    groups.get_group("g1")
    groups.create_group({"name": "g"})
    groups.update_group("g2", {"name": "g2"})
    groups.archive_group("g3")
    groups.restore_group("g4")
    groups.get_group_projects("g5", params={"limit": 1})
    groups.get_group_vulnerabilities("g6", params={"limit": 1})

    assert transport.calls[0][1] == "/api/ss/groups"
    assert transport.calls[1][1] == "/api/ss/group/g1"
    assert transport.calls[2][1] == "/api/ss/group"
    assert transport.calls[3][1] == "/api/ss/group/g2"
    assert transport.calls[4][1] == "/api/ss/group/g3/archive"
    assert transport.calls[5][1] == "/api/ss/group/g4/restore"
    assert transport.calls[6][1] == "/api/ss/groups/g5/projects"
    assert transport.calls[7][1] == "/api/ss/groups/g6/vulnerabilities"


def test_projects_get_projects_by_group():
    transport = FakeTransport()
    projects = ProjectsResource(transport)
    projects.get_projects_by_group("g1", params={"limit": 10})

    assert transport.calls[0][1] == "/api/ss/groups/g1/projects"
    assert transport.calls[0][2]["params"]["limit"] == 10


def test_findings_get_vulnerabilities_by_group():
    transport = FakeTransport()
    findings = FindingsResource(transport)
    findings.get_vulnerabilities_by_group("g1", params={"limit": 5})

    assert transport.calls[0][1] == "/api/ss/groups/g1/vulnerabilities"
    assert transport.calls[0][2]["params"]["limit"] == 5


def test_projects_upload_workspace_file():
    transport = FakeTransport()
    projects = ProjectsResource(transport)
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(b"data")
        path = tmp.name
    try:
        projects.upload_workspace_file("p1", path)
        method, path_used, kwargs = transport.calls[0]
        assert method == "POST"
        assert path_used == "/api/ss/project/p1/workspace/file"
        assert "files" in kwargs
    finally:
        os.remove(path)


def test_findings_resource_calls_and_upsert():
    transport = FakeTransport()
    findings = FindingsResource(transport)
    findings.create_vulnerability({"projectId": "p"})
    findings.create_vulnerability_bulk({"items": []})
    findings.create_vulnerability_with_library({"projectId": "p"})
    findings.get_vulnerabilities()
    findings.get_vulnerability("v1")
    findings.get_project_vulnerabilities("p1")
    findings.get_vulnerabilities_by_asset_name("a1")
    findings.update_vulnerability("v2", {"title": "x"})
    findings.update_vulnerability_with_library("v3", {"title": "y"})
    findings.update_vulnerability_slas({"items": []})
    findings.update_linked_projects_on_vulnerabilities({"items": []})
    findings.get_vulnerability_revision_history("v4")

    assert transport.calls[0][1] == "/api/ss/vulnerability"
    assert transport.calls[2][1] == "/api/ss/vulnerability-with-library"
    assert transport.calls[5][1] == "/api/ss/project/p1/vulnerabilities"
    assert transport.calls[6][1] == "/api/ss/vulnerabilities/asset"
    assert transport.calls[10][1] == "/api/ss/vulnerabilities/projects"

    # Upsert: existing finding with one asset
    findings.get_project_vulnerabilities_all = lambda project_id, **kwargs: [
        {
            "vulnerability_id": "v100",
            "vulnerability_title": "Test Finding",
            "vulnerability_affected_assets": [{"asset": {"name": "asset-a"}}],
        }
    ]
    findings.update_vulnerability = lambda vid, payload: {"id": vid, "payload": payload}
    findings.get_vulnerability = lambda vid: {
        "vulnerability_affected_assets": [
            {"asset": {"name": "asset-a"}},
            {"asset": {"name": "asset-b"}},
        ]
    }

    result = findings.upsert_finding_by_title(
        project_id="p1",
        title="  test finding ",
        affected_assets=["asset-a", "asset-b"],
        create_payload={"projectId": "p1"},
    )
    assert result["action"] == "update"
    assert "asset-b" in result["added_assets"]


def test_findings_upload_and_fifo():
    transport = FakeTransport()
    findings = FindingsResource(transport)

    def fake_get_vuln(vuln_id):
        return {
            "evidence": [
                {"file": "old1.png", "created": "2024-01-01T00:00:00Z"},
                {"file": "old2.png", "created": "2024-02-01T00:00:00Z"},
            ]
        }

    findings.get_vulnerability = fake_get_vuln
    deleted = []
    findings.delete_vulnerability_evidence = lambda vid, fname: deleted.append(fname)

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(b"data")
        path = tmp.name
    try:
        findings.upload_vulnerability_evidence("v1", path, keep_last=1)
        assert deleted == ["old1.png"]
    finally:
        os.remove(path)


def test_writeups_resource_calls():
    transport = FakeTransport()
    writeups = WriteupsResource(transport)
    writeups.get_writeups()
    writeups.create_writeup({"title": "t"})
    writeups.update_writeup("w1", {"title": "u"})
    writeups.download_writeup_file("w2", "file.pdf")

    assert transport.calls[0][1] == "/api/ss/library"
    assert transport.calls[1][1] == "/api/ss/library/vulnerability"
    assert transport.calls[2][1] == "/api/ss/library/w1"
    assert transport.calls[3][1] == "/api/ss/library/w2/file/file.pdf"


def test_writeups_upload_file():
    transport = FakeTransport()
    writeups = WriteupsResource(transport)
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(b"data")
        path = tmp.name
    try:
        writeups.upload_writeup_file("w1", path)
        method, path_used, kwargs = transport.calls[0]
        assert method == "POST"
        assert path_used == "/api/ss/library/w1/file"
        assert "files" in kwargs
    finally:
        os.remove(path)


def test_testcases_resource_calls_and_touch():
    transport = FakeTransport()
    testcases = TestcasesResource(transport)
    testcases.create_testcase("p1", {"testcase": "t"})
    testcases.get_project_testcases("p2")
    testcases.update_testcase("p3", "tc1", {"status": "Tested"})
    testcases.create_testcase_note("p4", "tc2", {"note": "x"})
    testcases.download_testcase_file("p5", "tc3", "file.png")
    testcases.download_testcase_note_file("p6", "n1", "note.txt")
    testcases.download_testcase_workspace_note_file("p7", "n2", "note.txt")
    testcases.delete_testcase_file("p8", "tc4", "file.png")

    assert transport.calls[0][1] == "/api/ss/project/p1/testcase"
    assert transport.calls[1][1] == "/api/ss/project/p2/testcases"
    assert transport.calls[2][1] == "/api/ss/project/p3/testcase/tc1"
    assert transport.calls[3][1] == "/api/ss/project/p4/testcase/tc2/note"
    assert transport.calls[4][1] == "/api/ss/project/p5/testcase/tc3/file/file.png"
    assert transport.calls[7][1] == "/api/ss/project/p8/testcase/tc4/file/file.png"


def test_touch_testcase_merge_and_overwrite():
    transport = FakeTransport()
    testcases = TestcasesResource(transport)
    testcases._find_testcase = lambda project_id, testcase_id: {
        "project_testcase_custom_fields": [
            {"key": "foo", "value": "bar"},
            {"key": "last_tested", "value": "old"},
        ]
    }

    testcases.touch_testcase("p1", "tc1", timestamp="2024-01-01T00:00:00Z")
    method, path, kwargs = transport.calls[-1]
    payload = kwargs["json"]
    keys = {item["key"] for item in payload["project_testcase_custom_fields"]}
    assert method == "PUT"
    assert path == "/api/ss/project/p1/testcase/tc1"
    assert keys == {"foo", "last_tested", "testcase_type"}
    last_tested = next(
        item for item in payload["project_testcase_custom_fields"] if item["key"] == "last_tested"
    )
    assert last_tested["value"] == "2024-01-01T00:00:00Z"
    testcase_type = next(
        item for item in payload["project_testcase_custom_fields"] if item["key"] == "testcase_type"
    )
    assert testcase_type["value"] == "Security Test Case"

    testcases.touch_testcase("p1", "tc1", timestamp="2024-02-01T00:00:00Z", overwrite=True)
    method, path, kwargs = transport.calls[-1]
    payload = kwargs["json"]
    assert payload["project_testcase_custom_fields"] == [
        {"key": "last_tested", "value": "2024-02-01T00:00:00Z"},
        {"key": "testcase_type", "value": "Security Test Case"},
    ]


def test_testcases_upload_and_fifo():
    transport = FakeTransport()
    testcases = TestcasesResource(transport)

    testcases._find_testcase = lambda project_id, testcase_id: {
        "files": [
            {"file": "old1.png", "created": "2024-01-01T00:00:00Z"},
            {"file": "old2.png", "created": "2024-02-01T00:00:00Z"},
        ]
    }
    deleted = []
    testcases.delete_testcase_file = lambda p, t, f: deleted.append(f)

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(b"data")
        path = tmp.name
    try:
        testcases.upload_testcase_file("p1", "tc1", path, keep_last=1)
        assert deleted == ["old1.png"]
    finally:
        os.remove(path)


def test_testsuites_resource_calls():
    transport = FakeTransport()
    testsuites = TestsuitesResource(transport)
    testsuites.create_testsuite({"name": "ts"})
    testsuites.get_testsuites()
    testsuites.get_testsuite("ts1")
    testsuites.update_testsuite("ts2", {"name": "u"})
    testsuites.add_testcase_to_testsuite("ts3", {"testcase": "x"})
    testsuites.add_testcases_to_testsuite("ts4", {"testcases": []})
    testsuites.update_testcase_on_testsuite("ts5", "tc1", {"status": "Tested"})
    testsuites.download_testsuite_testcase_file("ts6", "tc2", "file.png")

    assert transport.calls[0][1] == "/api/ss/testsuite"
    assert transport.calls[1][1] == "/api/ss/testsuites"
    assert transport.calls[2][1] == "/api/ss/testsuites/ts1"
    assert transport.calls[6][1] == "/api/ss/testsuite/ts5/testcase/tc1"
    assert transport.calls[7][1] == "/api/ss/testsuites/ts6/testcase/tc2/file/file.png"


def test_testsuites_upload_file():
    transport = FakeTransport()
    testsuites = TestsuitesResource(transport)
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(b"data")
        path = tmp.name
    try:
        testsuites.upload_testsuite_testcase_file("ts1", "tc1", path)
        method, path_used, kwargs = transport.calls[0]
        assert method == "POST"
        assert path_used == "/api/ss/testsuites/ts1/testcase/tc1/file"
        assert "files" in kwargs
    finally:
        os.remove(path)


def test_notes_resource_calls():
    transport = FakeTransport()
    notes = NotesResource(transport)
    notes.create_remediation_note("v1", {"note": "x"})
    notes.update_remediation_note("v2", "n1", {"note": "y"})
    notes.download_remediation_note_file("v3", "n2", "file.txt")

    assert transport.calls[0][1] == "/api/ss/vulnerability/v1/remediationNote"
    assert transport.calls[1][1] == "/api/ss/vulnerability/v2/remediationNote/n1"
    assert transport.calls[2][1] == "/api/ss/vulnerability/v3/remediationNote/n2/file/file.txt"


def test_notes_upload_file():
    transport = FakeTransport()
    notes = NotesResource(transport)
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(b"data")
        path = tmp.name
    try:
        notes.upload_remediation_note_file("v1", "n1", path)
        method, path_used, kwargs = transport.calls[0]
        assert method == "POST"
        assert path_used == "/api/ss/vulnerability/v1/remediationNote/n1/file"
        assert "files" in kwargs
    finally:
        os.remove(path)


def test_users_resource_calls():
    transport = FakeTransport()
    users = UsersResource(transport)
    users.create_user({"email": "a"})
    users.create_users([{"email": "bulk@example.com"}])
    users.get_user("u1")
    users.get_users()
    users.get_user_by_email("a@b.com")
    users.get_user_by_username("user")
    users.update_user("u2", {"email": "x"})
    users.activate_user("u3")
    users.deactivate_user("u4")
    users.add_user_to_group({"user_id": "u5"})
    users.update_user_access_on_group("u6", {"access_level": "Edit"})
    users.get_user_groups("u7")
    users.get_user_projects("u8")
    users.get_user_audit_logs("u9")
    users.get_user_login_history("u10")

    assert transport.calls[0][1] == "/api/ss/user"
    assert transport.calls[1][1] == "/api/ss/users"
    assert transport.calls[2][1] == "/api/ss/users/u1"
    assert transport.calls[4][1].startswith("/api/ss/users/email/")
    assert transport.calls[7][1] == "/api/ss/user/u3/activate"
    assert transport.calls[10][1] == "/api/ss/group/user/u6"
    assert transport.calls[13][1] == "/api/ss/user/u9/auditlogs"
    assert transport.calls[14][1] == "/api/ss/user/u10/logins"


def test_reports_resource_calls():
    transport = FakeTransport()
    reports = ReportsResource(transport)
    reports.get_project_report("p1", "raw")
    reports.get_project_report_data("p2", "csv", {"vulnerabilityIds": []})
    reports.update_exec_summary_notes("p3", {"exec_summary_notes": "x"})

    assert transport.calls[0][1] == "/api/ss/project/p1/report/raw"
    assert transport.calls[1][1] == "/api/ss/project/p2/report/csv"
    assert transport.calls[2][1] == "/api/ss/project/p3/execSummaryNotes"
