"""
Unit tests for use cases catalog (45 use cases verification).
"""
import os
import yaml

def test_use_cases_catalog():
    catalog_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "..", "use_cases", "catalog.yaml")
    )
    assert os.path.exists(catalog_path), f"catalog.yaml not found at {catalog_path}"

    with open(catalog_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    use_cases = data.get("use_cases", [])
    assert len(use_cases) == 45, f"Expected 45 use cases, found {len(use_cases)}"

    # Check all use case IDs are unique
    ids = [uc["id"] for uc in use_cases]
    assert len(ids) == len(set(ids)), "Duplicate use case IDs found!"

    # Verify shared use cases
    uc24 = next((uc for uc in use_cases if uc["id"] == "UC-24"), None)
    assert uc24 is not None
    assert uc24["shared"] is True
    assert "A11_devops_platform" in uc24["shared_with"]

    uc43 = next((uc for uc in use_cases if uc["id"] == "UC-43"), None)
    assert uc43 is not None
    assert uc43["shared"] is True
    assert "A12_employee_services" in uc43["shared_with"]
