"""Excel parser for knowledge base ingestion."""

from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd

from ..common.logging import get_logger
from ..common.schemas import Framework, KnowledgeChunk, Language
from ..common.utils import generate_id, normalize_text, extract_control_id

logger = get_logger(__name__)


class ExcelParser:
    """
    Parser for Excel files containing controls, requirements, and mappings.

    Supports multiple formats:
    - Controls sheets (control_id, title, requirements, guidance, evidence)
    - Requirements sheets (requirement_id, description, category)
    - Mapping sheets (source_control, target_control, framework_mapping)
    - Tracker sheets (implementation status, progress, notes)
    """

    def __init__(self):
        """Initialize Excel parser."""
        self.logger = logger

    async def parse_controls_file(
        self,
        file_path: Path,
        framework: Framework,
        language: Language = Language.ARABIC
    ) -> List[KnowledgeChunk]:
        """
        Parse controls Excel file.

        Expected columns:
        - control_id or Control ID
        - control_title or Title (AR/EN)
        - requirements or Requirements
        - implementation_guidance or Guidance
        - expected_evidence or Evidence

        Args:
            file_path: Path to Excel file
            framework: Framework name
            language: Language of content

        Returns:
            List of knowledge chunks
        """
        logger.info(f"Parsing controls file: {file_path}")

        try:
            # Read Excel file
            df = pd.read_excel(file_path, sheet_name=0)

            # Normalize column names
            df.columns = [col.lower().strip().replace(" ", "_") for col in df.columns]

            chunks = []

            for idx, row in df.iterrows():
                # Extract control ID
                control_id = self._get_column_value(row, ["control_id", "id", "control_no"])

                if not control_id or pd.isna(control_id):
                    continue

                control_id = str(control_id).strip()

                # Extract control title
                title = self._get_column_value(
                    row,
                    ["control_title", "title", "control_name", "name"]
                )

                # Extract requirements
                requirements = self._get_column_value(
                    row,
                    ["requirements", "requirement", "description", "desc"]
                )

                # Extract guidance
                guidance = self._get_column_value(
                    row,
                    ["implementation_guidance", "guidance", "implementation", "notes"]
                )

                # Extract evidence
                evidence = self._get_column_value(
                    row,
                    ["expected_evidence", "evidence", "required_evidence"]
                )

                # Create control chunk
                control_text = f"{control_id}: {title}"
                if requirements and not pd.isna(requirements):
                    control_text += f"\n\nRequirements: {requirements}"
                if guidance and not pd.isna(guidance):
                    control_text += f"\n\nGuidance: {guidance}"

                chunks.append(KnowledgeChunk(
                    chunk_id=generate_id(f"{framework.value}_{control_id}_"),
                    framework=framework,
                    type="control",
                    id=control_id,
                    lang=language,
                    text=normalize_text(control_text, language.value),
                    metadata={
                        "title": str(title) if title else "",
                        "requirements": str(requirements) if requirements else "",
                        "guidance": str(guidance) if guidance else "",
                        "evidence": str(evidence) if evidence else "",
                        "source_file": str(file_path),
                        "row_number": idx + 2
                    }
                ))

                # Create separate evidence chunk if exists
                if evidence and not pd.isna(evidence):
                    evidence_text = f"{control_id} - Evidence Requirements: {evidence}"

                    chunks.append(KnowledgeChunk(
                        chunk_id=generate_id(f"{framework.value}_{control_id}_evidence_"),
                        framework=framework,
                        type="evidence",
                        id=control_id,
                        lang=language,
                        text=normalize_text(evidence_text, language.value),
                        metadata={
                            "control_id": control_id,
                            "evidence_list": str(evidence),
                            "source_file": str(file_path),
                            "row_number": idx + 2
                        }
                    ))

            logger.info(f"Parsed {len(chunks)} chunks from {file_path}")

            return chunks

        except Exception as e:
            logger.error(f"Error parsing controls file {file_path}: {e}", exc_info=True)
            raise

    async def parse_mapping_file(
        self,
        file_path: Path,
        source_framework: Framework,
        target_framework: Framework
    ) -> List[KnowledgeChunk]:
        """
        Parse framework mapping Excel file.

        Expected columns:
        - source_control_id
        - target_control_id
        - mapping_type (direct, partial, related)
        - notes

        Args:
            file_path: Path to Excel file
            source_framework: Source framework
            target_framework: Target framework

        Returns:
            List of mapping chunks
        """
        logger.info(f"Parsing mapping file: {file_path}")

        try:
            df = pd.read_excel(file_path, sheet_name=0)
            df.columns = [col.lower().strip().replace(" ", "_") for col in df.columns]

            chunks = []

            for idx, row in df.iterrows():
                source_id = self._get_column_value(
                    row,
                    ["source_control_id", "source_id", "source"]
                )
                target_id = self._get_column_value(
                    row,
                    ["target_control_id", "target_id", "target"]
                )

                if not source_id or not target_id or pd.isna(source_id) or pd.isna(target_id):
                    continue

                mapping_type = self._get_column_value(row, ["mapping_type", "type"])
                notes = self._get_column_value(row, ["notes", "note", "description"])

                mapping_text = f"Mapping: {source_framework.value} {source_id} -> {target_framework.value} {target_id}"
                if mapping_type:
                    mapping_text += f" (Type: {mapping_type})"
                if notes:
                    mapping_text += f"\nNotes: {notes}"

                chunks.append(KnowledgeChunk(
                    chunk_id=generate_id(f"mapping_{source_id}_{target_id}_"),
                    framework=source_framework,
                    type="mapping",
                    id=f"{source_id}→{target_id}",
                    lang=Language.ENGLISH,
                    text=mapping_text,
                    metadata={
                        "source_framework": source_framework.value,
                        "target_framework": target_framework.value,
                        "source_id": str(source_id),
                        "target_id": str(target_id),
                        "mapping_type": str(mapping_type) if mapping_type else "direct",
                        "notes": str(notes) if notes else "",
                        "source_file": str(file_path),
                        "row_number": idx + 2
                    }
                ))

            logger.info(f"Parsed {len(chunks)} mapping chunks from {file_path}")

            return chunks

        except Exception as e:
            logger.error(f"Error parsing mapping file {file_path}: {e}", exc_info=True)
            raise

    def _get_column_value(
        self,
        row: pd.Series,
        possible_names: List[str]
    ) -> Optional[Any]:
        """
        Get value from row by trying multiple column names.

        Args:
            row: Pandas Series (row)
            possible_names: List of possible column names

        Returns:
            Column value or None
        """
        for name in possible_names:
            if name in row.index:
                value = row[name]
                if not pd.isna(value):
                    return value

        return None
