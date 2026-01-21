"""Document agent for generating DOCX files."""

from typing import Any, Dict

from ..common.schemas import ClientProfile, DocumentContent, Language
from .base import BaseAgent


class DocumentAgent(BaseAgent):
    """
    Document agent for generating DOCX documents.

    Responsibilities:
    - Load DOCX templates
    - Fill templates with generated content
    - Apply formatting and styles
    - Save final documents
    """

    def __init__(self):
        """Initialize document agent."""
        super().__init__("document")
        self.doc_service = None  # Will be initialized later

    async def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute document generation.

        Args:
            inputs: Contains document_content, template_name, client_profile

        Returns:
            Generated document path and metadata
        """
        document_content: DocumentContent = inputs.get("document_content")
        template_name: str = inputs.get("template_name", "default_policy")
        client_profile: ClientProfile = inputs.get("client_profile")
        language: Language = inputs.get("language", Language.ARABIC)

        if not document_content:
            raise ValueError("Document content is required")

        self.add_message(f"Generating DOCX document using template: {template_name}")

        # Load template
        template_path = await self._get_template_path(template_name, language)
        self.add_message(f"Using template: {template_path}")

        # Generate document
        output_path = await self._generate_document(
            template_path,
            document_content,
            client_profile
        )

        self.add_message(f"Document generated: {output_path}")

        return {
            "output_path": output_path,
            "template_used": template_name,
            "language": language,
            "client": client_profile.client_name
        }

    async def _get_template_path(
        self,
        template_name: str,
        language: Language
    ) -> str:
        """
        Get template file path.

        Args:
            template_name: Template name
            language: Language

        Returns:
            Template file path
        """
        from ..common.config import settings

        lang_suffix = "ar" if language == Language.ARABIC else "en"
        template_file = f"{template_name}_{lang_suffix}.docx"
        template_path = settings.templates_path / "policies" / template_file

        # Fallback to default if not found
        if not template_path.exists():
            template_path = settings.templates_path / "policies" / f"default_{lang_suffix}.docx"

        return str(template_path)

    async def _generate_document(
        self,
        template_path: str,
        content: DocumentContent,
        client_profile: ClientProfile
    ) -> str:
        """
        Generate DOCX document from template.

        Args:
            template_path: Path to template
            content: Document content
            client_profile: Client profile

        Returns:
            Path to generated document
        """
        from pathlib import Path
        from ..common.config import settings
        from ..common.utils import generate_id, sanitize_filename

        # TODO: Implement actual document generation
        # For now, return a mock path

        doc_id = generate_id("doc_")
        filename = sanitize_filename(f"{content.title}_{doc_id}.docx")
        output_dir = settings.clients_path / client_profile.client_id / "outputs"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / filename

        # Placeholder: In real implementation, use python-docx to:
        # 1. Load template
        # 2. Replace placeholders
        # 3. Insert sections
        # 4. Apply formatting
        # 5. Save document

        self.logger.info(f"Would generate document at: {output_path}")

        return str(output_path)
