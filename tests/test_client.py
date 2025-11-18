import unittest
from pyattackforge import PyAttackForgeClient


class TestPyAttackForgeClient(unittest.TestCase):
    def setUp(self):
        # Use dummy values for dry-run mode
        self.client = PyAttackForgeClient(api_key="dummy", dry_run=True)
        # Patch create_asset to return a dummy dict
        self.client.create_asset = lambda asset_data: {
            "name": asset_data.get("name", "DummyAsset")
        }

    def test_get_assets_dry_run(self):
        assets = self.client.get_assets()
        self.assertIsInstance(assets, dict)

    def test_create_asset_dry_run(self):
        asset = self.client.create_asset({"name": "TestAsset"})
        self.assertIsInstance(asset, dict)

    def test_get_project_by_name_dry_run(self):
        project = self.client.get_project_by_name("TestProject")
        self.assertIsNone(project)

    def test_create_project_dry_run(self):
        project = self.client.create_project("TestProject")
        self.assertIsInstance(project, dict)

    def test_create_vulnerability_dry_run(self):
        # Patch get_all_writeups to return a matching writeup for this test
        self.client.get_all_writeups = (
            lambda force_refresh=False: [
                {
                    "title": "Test Vuln",
                    "belongs_to_library": "Main Vulnerabilities",
                    "reference_id": "dummy_writeup_id",
                }
            ]
        )
        self.client.create_writeup = lambda **kwargs: {"reference_id": "dummy_writeup_id"}
        vuln = self.client.create_vulnerability(
            project_id="dummy",
            title="Test Vuln",
            affected_assets=[{"name": "TestAsset"}],
            priority="High",
            likelihood_of_exploitation=5,
            description="Test description",
            attack_scenario="Test scenario",
            remediation_recommendation="Test remediation",
            steps_to_reproduce="Step 1"
        )
        self.assertIsInstance(vuln, dict)

    def test_create_vulnerability_with_import_source_and_writeup_custom_fields(self):
        # Patch get_all_writeups to return a matching writeup for this test
        self.client.get_all_writeups = (
            lambda force_refresh=False: [
                {
                    "title": "Test Vuln 2",
                    "belongs_to_library": "Main Vulnerabilities",
                    "reference_id": "dummy_writeup_id",
                }
            ]
        )
        self.client.create_writeup = lambda **kwargs: {"reference_id": "dummy_writeup_id"}
        vuln = self.client.create_vulnerability(
            project_id="dummy",
            title="Test Vuln 2",
            affected_assets=[
                {"name": "TestAsset2"},
                {"name": "TestAsset3"}
            ],
            priority="Medium",
            likelihood_of_exploitation=3,
            description="Another test description",
            attack_scenario="Another scenario",
            remediation_recommendation="Another remediation",
            steps_to_reproduce="Step A",
            import_source="UnitTestSource",
            writeup_custom_fields=[
                {"key": "extra_info", "value": "unit test"}
            ]
        )
        self.assertIsInstance(vuln, dict)

    def test_create_vulnerability_old_dry_run(self):
        vuln = self.client.create_vulnerability_old(
            project_id="dummy",
            title="Legacy Vuln",
            affected_asset_name="LegacyAsset",
            priority="Low",
            likelihood_of_exploitation=1,
            description="Legacy description",
            attack_scenario="Legacy scenario",
            remediation_recommendation="Legacy remediation",
            steps_to_reproduce="Legacy step"
        )
        self.assertIsInstance(vuln, dict)

    def test_create_writeup_dry_run(self):
        writeup = self.client.create_writeup(
            title="SQL Injection",
            description="SQLi description",
            remediation_recommendation="Sanitize inputs",
            custom_fields=[
                {
                    "key": "references",
                    "value": "OWASP ASVS §5.3; CWE-89"
                }
            ]
        )
        self.assertIsInstance(writeup, dict)

    def test_create_finding_from_writeup_dry_run(self):
        finding = self.client.create_finding_from_writeup(
            project_id="dummy_project",
            writeup_id="dummy_writeup",
            priority="High",
            affected_assets=[
                {"name": "TestAsset4"},
                {"name": "TestAsset5"}
            ]
        )
        self.assertIsInstance(finding, dict)

    def test_get_findings_for_project_dry_run(self):
        findings = self.client.get_findings_for_project("dummy_project")
        self.assertIsInstance(findings, list)

    def test_upsert_finding_for_project_create(self):
        # Simulate no existing findings (should create new)
        self.client.get_findings_for_project = lambda project_id: []
        # Patch get_all_writeups to return a matching writeup for this test
        self.client.get_all_writeups = (
            lambda force_refresh=False: [
                {
                    "title": "UnitTest Finding",
                    "belongs_to_library": "Main Vulnerabilities",
                    "reference_id": "dummy_writeup_id",
                }
            ]
        )
        self.client.create_writeup = lambda **kwargs: {"reference_id": "dummy_writeup_id"}
        result = self.client.upsert_finding_for_project(
            project_id="dummy_project",
            title="UnitTest Finding",
            affected_assets=[{"name": "AssetA"}],
            priority="High",
            likelihood_of_exploitation=7,
            description="Test finding description",
            attack_scenario="Test scenario",
            remediation_recommendation="Test remediation",
            steps_to_reproduce="Step 1",
            tags=["unit", "test"],
            notes=[
                {"note": "Initial note", "type": "PLAINTEXT"}
            ],
        )
        self.assertIsInstance(result, dict)
        self.assertEqual(result.get("action"), "create")

    def test_upsert_finding_for_project_update(self):
        # Simulate an existing finding with the same title and some assets/notes
        existing_finding = {
            "vulnerability_id": "123",
            "vulnerability_title": "UnitTest Finding",
            "vulnerability_affected_assets": [
                {"asset": {"name": "AssetA"}},
                {"asset": {"name": "AssetB"}}
            ],
            "vulnerability_notes": [{"note": "Existing note", "type": "PLAINTEXT"}]
        }
        self.client.get_findings_for_project = lambda project_id: [existing_finding]
        # Patch get_all_writeups to return a matching writeup for this test
        self.client.get_all_writeups = (
            lambda force_refresh=False: [
                {
                    "title": "UnitTest Finding",
                    "belongs_to_library": "Main Vulnerabilities",
                    "reference_id": "dummy_writeup_id",
                }
            ]
        )
        self.client.create_writeup = lambda **kwargs: {"reference_id": "dummy_writeup_id"}
        # Patch _request to simulate API update response
        class Resp:
            status_code = 200
            def json(self):
                return {"updated": True}
            text = "OK"
        self.client._request = (
            lambda method, endpoint, json_data=None, params=None: Resp()
        )
        result = self.client.upsert_finding_for_project(
            project_id="dummy_project",
            title="UnitTest Finding",
            affected_assets=[
                {"name": "AssetB"},
                {"name": "AssetC"}
            ],
            priority="High",
            likelihood_of_exploitation=7,
            description="Test finding description",
            attack_scenario="Test scenario",
            remediation_recommendation="Test remediation",
            steps_to_reproduce="Step 1",
            tags=["unit", "test"],
            notes=[
                {"note": "Existing note", "type": "PLAINTEXT"},
                {"note": "New note", "type": "PLAINTEXT"}
            ],
        )
        self.assertIsInstance(result, dict)
        self.assertEqual(result.get("action"), "update")
        # Check that assets are merged and deduplicated
        update_payload = result.get("update_payload", {})
        asset_names = {
            a["assetName"] for a in update_payload.get("affected_assets", [])
        }
        self.assertSetEqual(asset_names, {"AssetA", "AssetB", "AssetC"})
        # Check that notes are merged and deduplicated
        notes = update_payload.get("notes", [])
        note_texts = {n["note"] for n in notes}
        self.assertSetEqual(note_texts, {"Existing note", "New note"})

    def test_find_writeup_in_cache_dry_run(self):
        writeup_id = self.client.find_writeup_in_cache("SQL Injection")
        self.assertTrue(writeup_id is None or isinstance(writeup_id, str))

    def test_project_scope_management_dry_run(self):
        # Patch _request to simulate API responses
        def fake_request(method, endpoint, json_data=None, params=None):
            if method == "get" and endpoint == "/api/ss/project/dummy_project":

                class Resp:
                    status_code = 200

                    def json(self):
                        return {"scope": ["AssetA", "AssetB"]}

                return Resp()
            if method == "put" and endpoint == "/api/ss/project/dummy_project":

                class Resp:
                    status_code = 200

                    def json(self):
                        return {"scope": json_data.get("scope", [])}

                return Resp()
            raise RuntimeError("Unexpected API call")
        self.client._request = fake_request
        # Test get_project_scope
        scope = self.client.get_project_scope("dummy_project")
        self.assertSetEqual(scope, {"AssetA", "AssetB"})
        # Test update_project_scope (add AssetC)
        updated = self.client.update_project_scope("dummy_project", ["AssetC"])
        self.assertIn("scope", updated)
        self.assertIn("AssetC", updated["scope"])

    def test_create_writeup_missing_required_fields(self):
        # Should raise ValueError if required fields are missing
        # Do not patch create_writeup here so real validation is used
        with self.assertRaises(ValueError):
            self.client.create_writeup(
                title="",
                description="desc",
                remediation_recommendation="remed"
            )
        with self.assertRaises(ValueError):
            self.client.create_writeup(
                title="Title",
                description="",
                remediation_recommendation="remed"
            )
        with self.assertRaises(ValueError):
            self.client.create_writeup(
                title="Title",
                description="desc",
                remediation_recommendation=""
            )

    def test_dummy_response(self):
        from pyattackforge.client import DummyResponse
        resp = DummyResponse()
        self.assertEqual(resp.status_code, 200)
        self.assertIsInstance(resp.json(), dict)
        self.assertIn("[DRY RUN]", resp.text)


if __name__ == "__main__":
    unittest.main()
