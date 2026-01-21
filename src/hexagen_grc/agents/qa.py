"""QA agent for quality assurance and compliance checking."""

from typing import Any, Dict, List

from ..common.schemas import DocumentContent, Framework, Language
from .base import LLMAgent


class QAAgent(LLMAgent):
    """
    QA agent for quality assurance.

    Responsibilities:
    - Check completeness of sections
    - Verify framework references
    - Check for inconsistencies
    - Provide quality score and feedback
    """

    def __init__(self):
        """Initialize QA agent."""
        super().__init__("qa")

    async def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute QA checks.

        Args:
            inputs: Contains document_content, frameworks

        Returns:
            QA results with score and issues
        """
        document_content: DocumentContent = inputs.get("document_content")
        frameworks: List[Framework] = inputs.get("frameworks", [])
        language: Language = inputs.get("language", Language.ARABIC)

        if not document_content:
            raise ValueError("Document content is required")

        self.add_message("Starting QA checks")

        # Run checks
        checks = {
            "completeness": await self._check_completeness(document_content),
            "references": await self._check_references(document_content, frameworks),
            "consistency": await self._check_consistency(document_content),
            "language_quality": await self._check_language_quality(document_content, language)
        }

        # Calculate overall score
        score = self._calculate_score(checks)

        # Collect issues
        issues = []
        for check_name, check_result in checks.items():
            if not check_result.get("passed", False):
                issues.extend(check_result.get("issues", []))

        self.add_message(f"QA Score: {score}/100")

        if issues:
            self.add_message(f"Found {len(issues)} issues", level="warning")
        else:
            self.add_message("No issues found")

        return {
            "score": score,
            "passed": score >= 70,
            "checks": checks,
            "issues": issues,
            "recommendations": self._generate_recommendations(checks, issues)
        }

    async def _check_completeness(
        self,
        content: DocumentContent
    ) -> Dict[str, Any]:
        """
        Check if all required sections are present.

        Args:
            content: Document content

        Returns:
            Check results
        """
        required_sections = [
            "purpose", "scope", "definitions", "roles",
            "requirements", "compliance", "review", "references"
        ]

        present_sections = []
        missing_sections = []

        for section in content.sections:
            section_type = section.section_id.lower()
            if any(req in section.title.lower() or req in section_type for req in required_sections):
                present_sections.append(section.title)

        for req in required_sections:
            if not any(req in s.lower() for s in present_sections):
                missing_sections.append(req)

        passed = len(missing_sections) == 0

        return {
            "passed": passed,
            "score": (len(present_sections) / len(required_sections)) * 100,
            "present": present_sections,
            "missing": missing_sections,
            "issues": [f"Missing section: {s}" for s in missing_sections]
        }

    async def _check_references(
        self,
        content: DocumentContent,
        frameworks: List[Framework]
    ) -> Dict[str, Any]:
        """
        Check if framework references are present.

        Args:
            content: Document content
            frameworks: Required frameworks

        Returns:
            Check results
        """
        issues = []
        references_found = []

        # Count references in all sections
        for section in content.sections:
            references_found.extend(section.references)

        # Check if each framework is referenced
        framework_coverage = {}
        for framework in frameworks:
            fw_refs = [ref for ref in references_found if framework.value in ref]
            framework_coverage[framework.value] = len(fw_refs)

            if len(fw_refs) == 0:
                issues.append(f"No references found for framework: {framework.value}")

        passed = len(issues) == 0
        total_refs = len(references_found)

        return {
            "passed": passed,
            "score": 100 if passed else 50,
            "total_references": total_refs,
            "framework_coverage": framework_coverage,
            "issues": issues
        }

    async def _check_consistency(
        self,
        content: DocumentContent
    ) -> Dict[str, Any]:
        """
        Check for consistency in content.

        Args:
            content: Document content

        Returns:
            Check results
        """
        issues = []

        # Check for empty sections
        for section in content.sections:
            if not section.content or len(section.content.strip()) < 50:
                issues.append(f"Section '{section.title}' is too short or empty")

        # Check for consistent terminology
        # TODO: Implement terminology checking

        passed = len(issues) == 0

        return {
            "passed": passed,
            "score": 100 if passed else 70,
            "issues": issues
        }

    async def _check_language_quality(
        self,
        content: DocumentContent,
        language: Language
    ) -> Dict[str, Any]:
        """
        Check language quality.

        Args:
            content: Document content
            language: Expected language

        Returns:
            Check results
        """
        issues = []

        # Basic checks
        for section in content.sections:
            # Check for mixed languages (basic)
            if language == Language.ARABIC:
                # Check if Arabic text is present
                arabic_chars = sum(1 for c in section.content if '\u0600' <= c <= '\u06FF')
                if arabic_chars < len(section.content) * 0.3:
                    issues.append(f"Section '{section.title}' may not be primarily in Arabic")
            else:
                # Check if English text is present
                english_chars = sum(1 for c in section.content if c.isascii())
                if english_chars < len(section.content) * 0.7:
                    issues.append(f"Section '{section.title}' may not be primarily in English")

        passed = len(issues) == 0

        return {
            "passed": passed,
            "score": 100 if passed else 80,
            "issues": issues
        }

    def _calculate_score(self, checks: Dict[str, Dict[str, Any]]) -> float:
        """
        Calculate overall QA score.

        Args:
            checks: Dictionary of check results

        Returns:
            Overall score (0-100)
        """
        scores = [check.get("score", 0) for check in checks.values()]
        return sum(scores) / len(scores) if scores else 0

    def _generate_recommendations(
        self,
        checks: Dict[str, Dict[str, Any]],
        issues: List[str]
    ) -> List[str]:
        """
        Generate recommendations based on QA results.

        Args:
            checks: Check results
            issues: List of issues

        Returns:
            List of recommendations
        """
        recommendations = []

        if not checks["completeness"]["passed"]:
            recommendations.append("Add missing sections to complete the document structure")

        if not checks["references"]["passed"]:
            recommendations.append("Add more framework references to support compliance claims")

        if not checks["consistency"]["passed"]:
            recommendations.append("Expand short sections and ensure consistent quality throughout")

        if not checks["language_quality"]["passed"]:
            recommendations.append("Review language consistency and quality")

        if not recommendations:
            recommendations.append("Document meets quality standards")

        return recommendations
