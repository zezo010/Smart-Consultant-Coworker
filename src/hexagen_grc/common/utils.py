"""Utility functions for HexaGen GRC."""

import hashlib
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import unicodedata


def generate_id(prefix: str = "", data: Optional[Dict[str, Any]] = None) -> str:
    """
    Generate a unique ID.

    Args:
        prefix: Optional prefix for the ID
        data: Optional data to hash

    Returns:
        Generated ID
    """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")

    if data:
        data_str = json.dumps(data, sort_keys=True)
        hash_suffix = hashlib.md5(data_str.encode()).hexdigest()[:8]
        return f"{prefix}{timestamp}_{hash_suffix}" if prefix else f"{timestamp}_{hash_suffix}"

    return f"{prefix}{timestamp}" if prefix else timestamp


def normalize_text(text: str, language: str = "ar") -> str:
    """
    Normalize text for processing.

    Args:
        text: Text to normalize
        language: Language code (ar/en)

    Returns:
        Normalized text
    """
    if not text:
        return ""

    # Unicode normalization
    text = unicodedata.normalize("NFKC", text)

    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text).strip()

    # Arabic-specific normalization
    if language == "ar":
        # Normalize Arabic characters
        text = text.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا")
        text = text.replace("ة", "ه")
        text = text.replace("ى", "ي")

    return text


def extract_control_id(text: str) -> Optional[str]:
    """
    Extract control ID from text.

    Args:
        text: Text containing control ID

    Returns:
        Extracted control ID or None
    """
    # Match patterns like: ECC-5-1-1, ISO27001:5.1, CCC-2.1, etc.
    patterns = [
        r"(ECC|CCC|DCC)-\d+(?:-\d+)*",
        r"ISO\d+:\d+(?:\.\d+)*",
        r"(PDPL|SAMA|NIS2)-\d+(?:\.\d+)*",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(0).upper()

    return None


def chunk_text(
    text: str,
    chunk_size: int = 512,
    chunk_overlap: int = 50,
    separators: Optional[List[str]] = None
) -> List[str]:
    """
    Split text into chunks.

    Args:
        text: Text to chunk
        chunk_size: Maximum chunk size
        chunk_overlap: Overlap between chunks
        separators: List of separators to split on

    Returns:
        List of text chunks
    """
    if not separators:
        separators = ["\n\n", "\n", ". ", ".", " "]

    chunks = []
    current_chunk = ""

    # Simple chunking implementation
    words = text.split()

    for word in words:
        if len(current_chunk) + len(word) + 1 <= chunk_size:
            current_chunk += " " + word if current_chunk else word
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = word

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename for safe file system usage.

    Args:
        filename: Original filename

    Returns:
        Sanitized filename
    """
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', "", filename)

    # Replace spaces with underscores
    filename = filename.replace(" ", "_")

    # Limit length
    name, ext = filename.rsplit(".", 1) if "." in filename else (filename, "")
    if len(name) > 200:
        name = name[:200]

    return f"{name}.{ext}" if ext else name


def read_json_file(file_path: Path) -> Dict[str, Any]:
    """
    Read JSON file.

    Args:
        file_path: Path to JSON file

    Returns:
        Parsed JSON data
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json_file(data: Dict[str, Any], file_path: Path) -> None:
    """
    Write JSON file.

    Args:
        data: Data to write
        file_path: Path to JSON file
    """
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def format_date(
    date: Optional[datetime] = None,
    language: str = "ar",
    format_type: str = "full"
) -> str:
    """
    Format date according to language.

    Args:
        date: Date to format (defaults to now)
        language: Language code (ar/en)
        format_type: Format type (full, short, iso)

    Returns:
        Formatted date string
    """
    if not date:
        date = datetime.now()

    if format_type == "iso":
        return date.isoformat()
    elif format_type == "short":
        return date.strftime("%Y-%m-%d")
    else:  # full
        if language == "ar":
            return date.strftime("%d/%m/%Y")
        else:
            return date.strftime("%B %d, %Y")


def merge_dicts(dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
    """
    Deep merge two dictionaries.

    Args:
        dict1: First dictionary
        dict2: Second dictionary (takes precedence)

    Returns:
        Merged dictionary
    """
    result = dict1.copy()

    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_dicts(result[key], value)
        else:
            result[key] = value

    return result
