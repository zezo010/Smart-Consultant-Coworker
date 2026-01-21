"""Tests for data schemas."""

import pytest
from hexagen_grc.common.schemas import (
    ClientProfile,
    GRCTaskRequest,
    Framework,
    Language,
    TaskType,
    DocumentType,
    KnowledgeChunk,
)


def test_client_profile_creation():
    """Test client profile creation."""
    profile = ClientProfile(
        client_id="test001",
        client_name="Test Company",
        client_name_ar="شركة الاختبار",
        industry="Technology",
        classification="Internal"
    )

    assert profile.client_id == "test001"
    assert profile.client_name == "Test Company"
    assert profile.classification == "Internal"


def test_grc_task_request_creation():
    """Test GRC task request creation."""
    profile = ClientProfile(
        client_id="test001",
        client_name="Test Company",
        industry="Technology"
    )

    request = GRCTaskRequest(
        task_type=TaskType.POLICY,
        client_profile=profile,
        frameworks=[Framework.NCA_ECC],
        language=Language.ARABIC,
        output_type=DocumentType.POLICY
    )

    assert request.task_type == TaskType.POLICY
    assert request.language == Language.ARABIC
    assert Framework.NCA_ECC in request.frameworks


def test_knowledge_chunk_creation():
    """Test knowledge chunk creation."""
    chunk = KnowledgeChunk(
        chunk_id="chunk_001",
        framework=Framework.NCA_ECC,
        type="control",
        id="ECC-5-1-1",
        lang=Language.ARABIC,
        text="This is a test control",
        metadata={"source": "test.xlsx"}
    )

    assert chunk.chunk_id == "chunk_001"
    assert chunk.framework == Framework.NCA_ECC
    assert chunk.type == "control"
    assert chunk.metadata["source"] == "test.xlsx"


def test_framework_enum():
    """Test framework enum."""
    assert Framework.NCA_ECC.value == "NCA_ECC"
    assert Framework.ISO_27001.value == "ISO_27001"

    # Test creation from string
    framework = Framework("NCA_ECC")
    assert framework == Framework.NCA_ECC


def test_language_enum():
    """Test language enum."""
    assert Language.ARABIC.value == "ar"
    assert Language.ENGLISH.value == "en"

    # Test creation from string
    lang = Language("ar")
    assert lang == Language.ARABIC


def test_task_type_enum():
    """Test task type enum."""
    assert TaskType.POLICY.value == "policy"
    assert TaskType.GAP_ANALYSIS.value == "gap_analysis"
