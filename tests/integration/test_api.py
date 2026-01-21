"""Integration tests for API."""

import pytest
from fastapi.testclient import TestClient

from hexagen_grc.api.main import app
from hexagen_grc.common.schemas import (
    Framework,
    Language,
    TaskType,
    DocumentType,
)


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


def test_root_endpoint(client):
    """Test root endpoint."""
    response = client.get("/")

    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data


def test_list_frameworks(client):
    """Test list frameworks endpoint."""
    response = client.get("/api/v1/frameworks")

    assert response.status_code == 200
    frameworks = response.json()
    assert isinstance(frameworks, list)
    assert "NCA_ECC" in frameworks


def test_list_templates(client):
    """Test list templates endpoint."""
    response = client.get("/api/v1/templates")

    assert response.status_code == 200
    templates = response.json()
    assert isinstance(templates, dict)
    assert "policies" in templates


def test_grc_task_creation(client, sample_client_profile):
    """Test GRC task creation."""
    request_data = {
        "task_type": "policy",
        "client_profile": sample_client_profile.model_dump(),
        "frameworks": ["NCA_ECC"],
        "language": "ar",
        "output_type": "policy",
        "parameters": {}
    }

    response = client.post("/api/v1/grc/task", json=request_data)

    assert response.status_code == 200
    data = response.json()
    assert "task_id" in data
    assert data["task_type"] == "policy"
