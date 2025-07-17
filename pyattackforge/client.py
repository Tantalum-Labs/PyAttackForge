import requests
from datetime import datetime, timezone, timedelta


class PyAttackForgeClient:
    def __init__(self, api_key, base_url="https://demo.attackforge.com", dry_run=False):
        self.base_url = base_url.rstrip("/")
        self.headers = {
            "X-SSAPI-KEY": api_key,
            "Content-Type": "application/json",
            "Connection": "close"
        }
        self.dry_run = dry_run
        self._asset_cache = None
        self._project_scope_cache = {}  # {project_id: set(asset_names)}

    def _request(self, method, endpoint, json_data=None, params=None):
        url = f"{self.base_url}{endpoint}"
        if self.dry_run:
            print(f"[DRY RUN] {method.upper()} {url}")
            if json_data:
                print("Payload:", json_data)
            if params:
                print("Params:", params)
            return DummyResponse()
        return requests.request(method, url, headers=self.headers, json=json_data, params=params)

    def get_assets(self):
        if self._asset_cache is None:
            self._asset_cache = {}
            skip, limit = 0, 500
            while True:
                resp = self._request("get", "/api/ss/assets", params={"skip": skip, "limit": limit})
                data = resp.json()
                for asset in data.get("assets", []):
                    name = asset.get("asset")
                    if name:
                        self._asset_cache[name] = asset
                if skip + limit >= data.get("count", 0):
                    break
                skip += limit
        return self._asset_cache

    def get_asset_by_name(self, name):
        return self.get_assets().get(name)

    def create_asset(self, asset_data):
        resp = self._request("post", "/api/ss/library/asset", json_data=asset_data)
        if resp.status_code == 201:
            asset = resp.json()
            self._asset_cache = None  # Invalidate cache
            return asset
        if "Asset Already Exists" in resp.text:
            return self.get_asset_by_name(asset_data["name"])
        raise RuntimeError(f"Asset creation failed: {resp.text}")

    def get_project_by_name(self, name):
        params = {
            "startDate": "2000-01-01T00:00:00.000Z",
            "endDate": "2100-01-01T00:00:00.000Z",
            "status": "All"
        }
        resp = self._request("get", "/api/ss/projects", params=params)
        for proj in resp.json().get("projects", []):
            if proj.get("project_name") == name:
                return proj
        return None

    def get_project_scope(self, project_id):
        if project_id in self._project_scope_cache:
            return self._project_scope_cache[project_id]

        resp = self._request("get", f"/api/ss/project/{project_id}")
        if resp.status_code != 200:
            raise RuntimeError(f"Failed to retrieve project: {resp.text}")

        scope = set(resp.json().get("scope", []))
        self._project_scope_cache[project_id] = scope
        return scope

    def update_project_scope(self, project_id, new_assets):
        current_scope = self.get_project_scope(project_id)
        updated_scope = list(current_scope.union(new_assets))
        resp = self._request("put", f"/api/ss/project/{project_id}", json_data={"scope": updated_scope})
        if resp.status_code not in (200, 201):
            raise RuntimeError(f"Failed to update project scope: {resp.text}")
        self._project_scope_cache[project_id] = set(updated_scope)
        return resp.json()

    def create_project(self, name, **kwargs):
        start, end = get_default_dates()
        payload = {
            "name": name,
            "code": kwargs.get("code", "DEFAULT"),
            "groups": kwargs.get("groups", []),
            "startDate": kwargs.get("startDate", start),
            "endDate": kwargs.get("endDate", end),
            "scope": kwargs.get("scope", []),
            "testsuites": kwargs.get("testsuites", []),
            "organization_code": kwargs.get("organization_code", "ORG_DEFAULT"),
            "vulnerability_code": kwargs.get("vulnerability_code", "VULN_"),
            "scoringSystem": kwargs.get("scoringSystem", "CVSSv3.1"),
            "team_notifications": kwargs.get("team_notifications", []),
            "admin_notifications": kwargs.get("admin_notifications", []),
            "custom_fields": kwargs.get("custom_fields", []),
            "asset_library_ids": kwargs.get("asset_library_ids", []),
            "sla_activation": kwargs.get("sla_activation", "automatic")
        }
        resp = self._request("post", "/api/ss/project", json_data=payload)
        if resp.status_code in (200, 201):
            return resp.json()
        raise RuntimeError(f"Project creation failed: {resp.text}")

    def update_project(self, project_id, update_fields):
        resp = self._request("put", f"/api/ss/project/{project_id}", json_data=update_fields)
        if resp.status_code in (200, 201):
            return resp.json()
        raise RuntimeError(f"Project update failed: {resp.text}")

    def create_vulnerability(
        self,
        vulnerability_data,
        auto_create_assets=False,
        default_asset_type="Placeholder",
        default_asset_library_ids=None
    ):
        affected_assets = vulnerability_data.get("affected_assets", [])
        project_id = vulnerability_data.get("projectId")
        if not project_id:
            raise ValueError("vulnerability_data must include 'projectId'")

        new_asset_names = []

        if auto_create_assets:
            for asset_ref in affected_assets:
                asset_name = asset_ref.get("assetName")
                if not asset_name:
                    continue
                if not self.get_asset_by_name(asset_name):
                    print(f"[INFO] Asset '{asset_name}' not found. Creating it.")
                    asset_payload = {
                        "name": asset_name,
                        "type": default_asset_type,
                        "external_id": asset_name,
                        "details": "Auto-created by PyAttackForge",
                        "groups": [],
                        "custom_fields": [],
                    }
                    if default_asset_library_ids:
                        asset_payload["asset_library_ids"] = default_asset_library_ids
                    self.create_asset(asset_payload)
                    new_asset_names.append(asset_name)

        if new_asset_names:
            print(f"[INFO] Adding {len(new_asset_names)} new assets to project '{project_id}' scope.")
            self.update_project_scope(project_id, new_asset_names)

        resp = self._request("post", "/api/ss/vulnerability", json_data=vulnerability_data)
        if resp.status_code in (200, 201):
            return resp.json()
        raise RuntimeError(f"Vulnerability creation failed: {resp.text}")


class DummyResponse:
    def __init__(self):
        self.status_code = 200

    def json(self):
        return {}


def get_default_dates():
    now = datetime.now(timezone.utc)
    start = now.isoformat(timespec="milliseconds").replace("+00:00", "Z")
    end = (now + timedelta(days=30)).isoformat(timespec="milliseconds").replace("+00:00", "Z")
    return start, end
