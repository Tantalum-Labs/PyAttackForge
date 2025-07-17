# PyAttackForge

A lightweight Python library for interacting with the AttackForge API.

---

## Features

- Create and fetch projects
- Manage assets
- Submit vulnerabilities
- Dry-run mode for testing

---

## Install

```bash
pip install git+https://github.com/Tantalum-Labs/PyAttackForge.git
```

---

## Use

```python
from pyattackforge.client import PyAttackForgeClient

# Initialize client - Note: Make sure to set your AttackForge URL and API Key
client = PyAttackForgeClient(api_key="your-api-key", base_url="https://demo.attackforge.com", dry_run=False)

# Create a project
project = client.create_project("My Project", scope=["Asset1", "Asset2"])

## Create a vulnerability with auto-created assets
client.create_vulnerability(
    vulnerability_data={
        "projectId": "abc123",
        "title": "Open SSH Port",
        "affected_assets": [{"assetName": "ssh-prod-1"}],
        "priority": "High",
        "likelihood_of_exploitation": 10,
        ...
    },
    auto_create_assets=True,
    default_asset_type="Cloud",
    default_asset_library_ids=["your-lib-id"]
)

```
