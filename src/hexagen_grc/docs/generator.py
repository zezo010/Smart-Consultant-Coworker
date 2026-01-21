"""Document generator for creating DOCX files from templates."""

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

from ..common.config import settings
from ..common.logging import get_logger
from ..common.schemas import ClientProfile, DocumentContent, DocumentSection, Language
from ..common.utils import format_date, generate_id, sanitize_filename

logger = get_logger(__name__)


class DocumentGenerator:
    """
    Document generator for creating DOCX files.

    Features:
    - Load DOCX templates
    - Replace placeholders
    - Insert generated sections
    - Apply formatting
    - Support Arabic RTL
    """

    def __init__(self):
        """Initialize document generator."""
        self.logger = logger

    async def generate_document(
        self,
        content: DocumentContent,
        template_name: str = "default_policy",
        output_dir: Optional[Path] = None
    ) -> Path:
        """
        Generate DOCX document from content.

        Args:
            content: Document content
            template_name: Template name
            output_dir: Optional output directory

        Returns:
            Path to generated document
        """
        logger.info(f"Generating document: {content.title}")

        # Get template path
        template_path = self._get_template_path(template_name, content.language)

        # Load template or create new document
        if template_path.exists():
            doc = Document(str(template_path))
            logger.info(f"Loaded template: {template_path}")
        else:
            doc = Document()
            logger.warning(f"Template not found, creating new document: {template_path}")

        # Replace placeholders
        self._replace_placeholders(doc, content)

        # Add sections
        self._add_sections(doc, content)

        # Determine output path
        if not output_dir:
            output_dir = settings.clients_path / content.client.client_id / "outputs"

        output_dir.mkdir(parents=True, exist_ok=True)

        doc_id = generate_id("doc_")
        filename = sanitize_filename(f"{content.title}_{doc_id}.docx")
        output_path = output_dir / filename

        # Save document
        doc.save(str(output_path))
        logger.info(f"Document saved: {output_path}")

        return output_path

    def _get_template_path(self, template_name: str, language: Language) -> Path:
        """
        Get template file path.

        Args:
            template_name: Template name
            language: Language

        Returns:
            Template path
        """
        lang_suffix = "ar" if language == Language.ARABIC else "en"
        template_file = f"{template_name}_{lang_suffix}.docx"
        template_path = settings.templates_path / "policies" / template_file

        # Fallback to default template
        if not template_path.exists():
            template_path = settings.templates_path / "policies" / f"default_{lang_suffix}.docx"

        return template_path

    def _replace_placeholders(self, doc: Document, content: DocumentContent) -> None:
        """
        Replace placeholders in document.

        Placeholders format: {{VARIABLE_NAME}}

        Args:
            doc: Document object
            content: Document content
        """
        # Build replacements dictionary
        replacements = {
            "{{CLIENT_NAME}}": content.client.client_name,
            "{{CLIENT_NAME_AR}}": content.client.client_name_ar or content.client.client_name,
            "{{CLIENT_NAME_EN}}": content.client.client_name_en or content.client.client_name,
            "{{DOCUMENT_TITLE}}": content.title,
            "{{VERSION}}": content.version,
            "{{CLASSIFICATION}}": content.classification,
            "{{DATE}}": format_date(datetime.now(), content.language.value),
            "{{INDUSTRY}}": content.client.industry,
            "{{SECTOR}}": content.client.sector or "",
        }

        # Add framework-specific replacements
        if content.frameworks:
            frameworks_str = ", ".join([f.value for f in content.frameworks])
            replacements["{{FRAMEWORKS}}"] = frameworks_str

        # Replace in paragraphs
        for paragraph in doc.paragraphs:
            for placeholder, value in replacements.items():
                if placeholder in paragraph.text:
                    paragraph.text = paragraph.text.replace(placeholder, value)

                    # Apply RTL for Arabic
                    if content.language == Language.ARABIC:
                        paragraph.paragraph_format.right_to_left = True

        # Replace in tables
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    for paragraph in cell.paragraphs:
                        for placeholder, value in replacements.items():
                            if placeholder in paragraph.text:
                                paragraph.text = paragraph.text.replace(placeholder, value)

                                if content.language == Language.ARABIC:
                                    paragraph.paragraph_format.right_to_left = True

    def _add_sections(self, doc: Document, content: DocumentContent) -> None:
        """
        Add generated sections to document.

        Args:
            doc: Document object
            content: Document content
        """
        # Find insertion point or add at end
        # Look for a placeholder like {{CONTENT}} or add after header

        insertion_paragraph = None
        for i, paragraph in enumerate(doc.paragraphs):
            if "{{CONTENT}}" in paragraph.text:
                insertion_paragraph = i
                paragraph.text = ""
                break

        if insertion_paragraph is None:
            # Add at end
            insertion_paragraph = len(doc.paragraphs)

        # Add each section
        for section in content.sections:
            # Add section heading
            heading = doc.add_paragraph(section.title)
            heading.style = "Heading 1"

            if content.language == Language.ARABIC:
                heading.paragraph_format.right_to_left = True

            # Add section content
            content_para = doc.add_paragraph(section.content)

            if content.language == Language.ARABIC:
                content_para.paragraph_format.right_to_left = True

            # Add references if any
            if section.references:
                refs_para = doc.add_paragraph()
                refs_para.add_run("References: ").bold = True
                refs_para.add_run(", ".join(section.references))

                if content.language == Language.ARABIC:
                    refs_para.paragraph_format.right_to_left = True

            # Add subsections
            if section.subsections:
                self._add_subsections(doc, section.subsections, content.language, level=2)

    def _add_subsections(
        self,
        doc: Document,
        subsections: List[DocumentSection],
        language: Language,
        level: int = 2
    ) -> None:
        """
        Add subsections to document.

        Args:
            doc: Document object
            subsections: List of subsections
            language: Language
            level: Heading level
        """
        heading_style = f"Heading {level}"

        for subsection in subsections:
            # Add subsection heading
            heading = doc.add_paragraph(subsection.title)
            heading.style = heading_style

            if language == Language.ARABIC:
                heading.paragraph_format.right_to_left = True

            # Add subsection content
            content_para = doc.add_paragraph(subsection.content)

            if language == Language.ARABIC:
                content_para.paragraph_format.right_to_left = True

            # Add references
            if subsection.references:
                refs_para = doc.add_paragraph()
                refs_para.add_run("References: ").bold = True
                refs_para.add_run(", ".join(subsection.references))

                if language == Language.ARABIC:
                    refs_para.paragraph_format.right_to_left = True

            # Recursively add nested subsections
            if subsection.subsections:
                self._add_subsections(doc, subsection.subsections, language, level + 1)

    async def create_simple_document(
        self,
        title: str,
        sections: List[Dict[str, str]],
        client_name: str,
        language: Language = Language.ARABIC,
        output_dir: Optional[Path] = None
    ) -> Path:
        """
        Create a simple document without using templates.

        Args:
            title: Document title
            sections: List of section dicts (title, content)
            client_name: Client name
            language: Language
            output_dir: Optional output directory

        Returns:
            Path to generated document
        """
        doc = Document()

        # Add title
        title_para = doc.add_paragraph(title)
        title_para.style = "Title"

        if language == Language.ARABIC:
            title_para.paragraph_format.right_to_left = True

        # Add client info
        info_para = doc.add_paragraph(f"Client: {client_name}")
        info_para.add_run(f"\nDate: {format_date(datetime.now(), language.value)}")

        if language == Language.ARABIC:
            info_para.paragraph_format.right_to_left = True

        doc.add_paragraph()  # Spacer

        # Add sections
        for section in sections:
            # Section heading
            heading = doc.add_paragraph(section.get("title", ""))
            heading.style = "Heading 1"

            if language == Language.ARABIC:
                heading.paragraph_format.right_to_left = True

            # Section content
            content = doc.add_paragraph(section.get("content", ""))

            if language == Language.ARABIC:
                content.paragraph_format.right_to_left = True

        # Save document
        if not output_dir:
            output_dir = settings.base_dir / "data" / "outputs"

        output_dir.mkdir(parents=True, exist_ok=True)

        doc_id = generate_id("doc_")
        filename = sanitize_filename(f"{title}_{doc_id}.docx")
        output_path = output_dir / filename

        doc.save(str(output_path))
        logger.info(f"Simple document created: {output_path}")

        return output_path
