"""Tests for common utilities."""

import pytest
from hexagen_grc.common.utils import (
    generate_id,
    normalize_text,
    extract_control_id,
    sanitize_filename,
    chunk_text,
)


def test_generate_id():
    """Test ID generation."""
    id1 = generate_id("test_")
    id2 = generate_id("test_")

    assert id1.startswith("test_")
    assert id2.startswith("test_")
    assert id1 != id2  # Should be unique


def test_generate_id_with_data():
    """Test ID generation with data."""
    data = {"key": "value"}
    id1 = generate_id("test_", data)
    id2 = generate_id("test_", data)

    assert id1.startswith("test_")
    assert id2.startswith("test_")
    # Same data should produce same hash
    assert id1.split("_")[-1] == id2.split("_")[-1]


def test_normalize_text_arabic():
    """Test Arabic text normalization."""
    text = "  مرحبا   بك   في   النظام  "
    normalized = normalize_text(text, "ar")

    assert normalized == "مرحبا بك في النظام"
    assert "  " not in normalized


def test_normalize_text_english():
    """Test English text normalization."""
    text = "  Hello   World  "
    normalized = normalize_text(text, "en")

    assert normalized == "Hello World"


def test_extract_control_id_ecc():
    """Test ECC control ID extraction."""
    text = "This is about control ECC-5-1-1 requirements"
    control_id = extract_control_id(text)

    assert control_id == "ECC-5-1-1"


def test_extract_control_id_iso():
    """Test ISO control ID extraction."""
    text = "Complies with ISO27001:5.1.2 requirements"
    control_id = extract_control_id(text)

    assert control_id == "ISO27001:5.1.2"


def test_extract_control_id_none():
    """Test control ID extraction with no match."""
    text = "No control ID in this text"
    control_id = extract_control_id(text)

    assert control_id is None


def test_sanitize_filename():
    """Test filename sanitization."""
    filename = "My Policy: Version 1.0.docx"
    sanitized = sanitize_filename(filename)

    assert ":" not in sanitized
    assert " " not in sanitized
    assert sanitized.endswith(".docx")


def test_sanitize_filename_long():
    """Test long filename sanitization."""
    filename = "A" * 300 + ".docx"
    sanitized = sanitize_filename(filename)

    # Name should be truncated but extension preserved
    assert len(sanitized) < len(filename)
    assert sanitized.endswith(".docx")


def test_chunk_text():
    """Test text chunking."""
    text = "Word " * 100
    chunks = chunk_text(text, chunk_size=50, chunk_overlap=10)

    assert len(chunks) > 0
    assert all(len(chunk) <= 50 for chunk in chunks)


def test_chunk_text_small():
    """Test chunking of small text."""
    text = "Short text"
    chunks = chunk_text(text, chunk_size=100)

    assert len(chunks) == 1
    assert chunks[0] == text
