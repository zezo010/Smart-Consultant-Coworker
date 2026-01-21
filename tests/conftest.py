"""Pytest configuration and fixtures."""

import pytest
from pathlib import Path
import tempfile
import shutil


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    # Cleanup
    shutil.rmtree(temp_path, ignore_errors=True)


@pytest.fixture
def sample_client_profile():
    """Sample client profile for testing."""
    from hexagen_grc.common.schemas import ClientProfile

    return ClientProfile(
        client_id="test001",
        client_name="Test Corporation",
        client_name_ar="شركة الاختبار",
        client_name_en="Test Corporation",
        industry="Financial Services",
        sector="Banking",
        classification="Internal"
    )


@pytest.fixture
def sample_controls_data():
    """Sample controls data for testing."""
    return [
        {
            "control_id": "ECC-5-1-1",
            "control_title_ar": "إدارة أمن المعلومات",
            "control_title_en": "Information Security Management",
            "requirements_ar": "يجب على المنشأة إنشاء نظام إدارة أمن المعلومات",
            "requirements_en": "The organization must establish an ISMS",
            "implementation_guidance_ar": "يجب أن يشمل النظام السياسات والإجراءات",
            "expected_evidence": "ISMS Policy, Framework Document"
        },
        {
            "control_id": "ECC-5-1-2",
            "control_title_ar": "سياسة أمن المعلومات",
            "control_title_en": "Information Security Policy",
            "requirements_ar": "يجب وضع سياسة معتمدة من الإدارة العليا",
            "requirements_en": "An approved policy must be established",
            "implementation_guidance_ar": "يجب مراجعة السياسة بشكل دوري",
            "expected_evidence": "Policy Document, Approval Records"
        }
    ]
