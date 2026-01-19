"""Ingestion service for knowledge base."""

from pathlib import Path
from typing import List, Optional

from ..common.config import settings
from ..common.logging import get_logger
from ..common.schemas import Framework, IngestionRequest, IngestionResult, KnowledgeChunk, Language
from ..common.utils import write_json_file
from ..kb.vector_store import VectorStore
from .excel_parser import ExcelParser

logger = get_logger(__name__)


class IngestionService:
    """
    Service for ingesting knowledge base files.

    Supports:
    - Excel files (controls, requirements, mappings)
    - PDF files (documentation)
    - DOCX files (templates, policies)
    """

    def __init__(self, vector_store: VectorStore):
        """
        Initialize ingestion service.

        Args:
            vector_store: Vector store instance
        """
        self.vector_store = vector_store
        self.excel_parser = ExcelParser()

    async def ingest_file(self, request: IngestionRequest) -> IngestionResult:
        """
        Ingest a file into knowledge base.

        Args:
            request: Ingestion request

        Returns:
            Ingestion result
        """
        file_path = Path(request.file_path)

        if not file_path.exists():
            return IngestionResult(
                framework=request.framework,
                chunks_created=0,
                file_processed=str(file_path),
                status="failed",
                errors=[f"File not found: {file_path}"]
            )

        logger.info(f"Ingesting file: {file_path}")

        try:
            # Parse file based on type
            chunks = await self._parse_file(
                file_path,
                request.framework,
                request.file_type,
                request.language
            )

            if not chunks:
                return IngestionResult(
                    framework=request.framework,
                    chunks_created=0,
                    file_processed=str(file_path),
                    status="success",
                    errors=["No chunks extracted from file"]
                )

            # Save chunks to JSON (for debugging/backup)
            await self._save_chunks_json(chunks, request.framework, file_path)

            # Add chunks to vector store
            chunks_added = await self.vector_store.add_chunks(chunks, request.framework)

            logger.info(f"Successfully ingested {chunks_added} chunks")

            return IngestionResult(
                framework=request.framework,
                chunks_created=chunks_added,
                file_processed=str(file_path),
                status="success",
                errors=[]
            )

        except Exception as e:
            logger.error(f"Error ingesting file {file_path}: {e}", exc_info=True)
            return IngestionResult(
                framework=request.framework,
                chunks_created=0,
                file_processed=str(file_path),
                status="failed",
                errors=[str(e)]
            )

    async def _parse_file(
        self,
        file_path: Path,
        framework: Framework,
        file_type: str,
        language: Optional[Language] = None
    ) -> List[KnowledgeChunk]:
        """
        Parse file based on type.

        Args:
            file_path: Path to file
            framework: Framework name
            file_type: Type of file (excel, pdf, docx)
            language: Optional language

        Returns:
            List of knowledge chunks
        """
        if not language:
            language = Language.ARABIC

        if file_type == "excel":
            return await self.excel_parser.parse_controls_file(
                file_path,
                framework,
                language
            )
        elif file_type == "pdf":
            # TODO: Implement PDF parsing
            logger.warning("PDF parsing not yet implemented")
            return []
        elif file_type == "docx":
            # TODO: Implement DOCX parsing
            logger.warning("DOCX parsing not yet implemented")
            return []
        else:
            raise ValueError(f"Unsupported file type: {file_type}")

    async def _save_chunks_json(
        self,
        chunks: List[KnowledgeChunk],
        framework: Framework,
        source_file: Path
    ) -> None:
        """
        Save chunks to JSON file for backup/debugging.

        Args:
            chunks: List of chunks
            framework: Framework name
            source_file: Source file path
        """
        output_dir = settings.kb_processed_path / framework.value
        output_dir.mkdir(parents=True, exist_ok=True)

        output_file = output_dir / f"{source_file.stem}_chunks.json"

        chunks_data = {
            "framework": framework.value,
            "source_file": str(source_file),
            "chunks_count": len(chunks),
            "chunks": [chunk.model_dump() for chunk in chunks]
        }

        write_json_file(chunks_data, output_file)
        logger.info(f"Saved chunks JSON to: {output_file}")

    async def ingest_directory(
        self,
        directory: Path,
        framework: Framework,
        language: Optional[Language] = None
    ) -> List[IngestionResult]:
        """
        Ingest all supported files in a directory.

        Args:
            directory: Directory path
            framework: Framework name
            language: Optional language

        Returns:
            List of ingestion results
        """
        logger.info(f"Ingesting directory: {directory}")

        if not directory.exists() or not directory.is_dir():
            logger.error(f"Directory not found: {directory}")
            return []

        results = []

        # Find all Excel files
        for excel_file in directory.glob("*.xlsx"):
            if excel_file.name.startswith("~$"):  # Skip temp files
                continue

            request = IngestionRequest(
                framework=framework,
                file_path=str(excel_file),
                file_type="excel",
                language=language
            )

            result = await self.ingest_file(request)
            results.append(result)

        logger.info(f"Ingested {len(results)} files from directory")

        return results
