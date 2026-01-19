"""Policy agent for generating policy content."""

from typing import Any, Dict, List

from ..common.schemas import ClientProfile, DocumentSection, Framework, Language
from .base import LLMAgent


class PolicyAgent(LLMAgent):
    """
    Policy agent for generating policy documents.

    Responsibilities:
    - Generate policy content based on frameworks
    - Add control references
    - Structure content into sections
    - Support Arabic and English
    """

    def __init__(self):
        """Initialize policy agent."""
        super().__init__("policy")

    async def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute policy generation.

        Args:
            inputs: Contains client_profile, frameworks, language, context

        Returns:
            Generated policy content
        """
        client_profile: ClientProfile = inputs.get("client_profile")
        frameworks: List[Framework] = inputs.get("frameworks", [])
        language: Language = inputs.get("language", Language.ARABIC)
        policy_type: str = inputs.get("policy_type", "information_security")
        context: Dict[str, Any] = inputs.get("context", {})

        self.add_message(f"Generating {policy_type} policy in {language}")

        # Build policy structure
        sections = await self._generate_policy_sections(
            client_profile,
            frameworks,
            language,
            policy_type,
            context
        )

        # Generate content for each section
        generated_sections = []
        for section in sections:
            content = await self._generate_section_content(
                section,
                client_profile,
                frameworks,
                language,
                context
            )
            generated_sections.append(content)

        self.add_message(f"Generated {len(generated_sections)} sections")

        return {
            "policy_type": policy_type,
            "language": language,
            "frameworks": frameworks,
            "sections": generated_sections,
            "metadata": {
                "client": client_profile.client_name,
                "version": "1.0",
                "classification": client_profile.classification
            }
        }

    async def _generate_policy_sections(
        self,
        client_profile: ClientProfile,
        frameworks: List[Framework],
        language: Language,
        policy_type: str,
        context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Define policy structure/sections.

        Args:
            client_profile: Client profile
            frameworks: Frameworks to comply with
            language: Target language
            policy_type: Type of policy
            context: Additional context

        Returns:
            List of section definitions
        """
        # Standard policy structure (Big4 style)
        if language == Language.ARABIC:
            sections = [
                {"id": "1", "title": "الغرض", "type": "purpose"},
                {"id": "2", "title": "النطاق", "type": "scope"},
                {"id": "3", "title": "التعريفات", "type": "definitions"},
                {"id": "4", "title": "الأدوار والمسؤوليات", "type": "roles"},
                {"id": "5", "title": "متطلبات السياسة", "type": "requirements"},
                {"id": "6", "title": "الامتثال", "type": "compliance"},
                {"id": "7", "title": "المراجعة والتحديث", "type": "review"},
                {"id": "8", "title": "المراجع", "type": "references"}
            ]
        else:
            sections = [
                {"id": "1", "title": "Purpose", "type": "purpose"},
                {"id": "2", "title": "Scope", "type": "scope"},
                {"id": "3", "title": "Definitions", "type": "definitions"},
                {"id": "4", "title": "Roles and Responsibilities", "type": "roles"},
                {"id": "5", "title": "Policy Requirements", "type": "requirements"},
                {"id": "6", "title": "Compliance", "type": "compliance"},
                {"id": "7", "title": "Review and Update", "type": "review"},
                {"id": "8", "title": "References", "type": "references"}
            ]

        return sections

    async def _generate_section_content(
        self,
        section: Dict[str, Any],
        client_profile: ClientProfile,
        frameworks: List[Framework],
        language: Language,
        context: Dict[str, Any]
    ) -> DocumentSection:
        """
        Generate content for a policy section.

        Args:
            section: Section definition
            client_profile: Client profile
            frameworks: Frameworks
            language: Target language
            context: Knowledge context

        Returns:
            Generated document section
        """
        section_type = section["type"]
        section_title = section["title"]

        self.add_message(f"Generating section: {section_title}")

        # Build prompt based on section type
        prompt = self._build_section_prompt(
            section_type,
            section_title,
            client_profile,
            frameworks,
            language,
            context
        )

        # Generate content using LLM
        content = await self.generate_text(
            prompt=prompt,
            system_prompt=self._get_system_prompt(language),
            temperature=0.3
        )

        # Extract references from content
        references = self._extract_references(content, frameworks)

        return DocumentSection(
            section_id=section["id"],
            title=section_title,
            content=content,
            references=references
        )

    def _build_section_prompt(
        self,
        section_type: str,
        section_title: str,
        client_profile: ClientProfile,
        frameworks: List[Framework],
        language: Language,
        context: Dict[str, Any]
    ) -> str:
        """
        Build prompt for section generation.

        Args:
            section_type: Type of section
            section_title: Section title
            client_profile: Client profile
            frameworks: Frameworks
            language: Target language
            context: Knowledge context

        Returns:
            Generated prompt
        """
        lang_name = "Arabic" if language == Language.ARABIC else "English"
        client_name = client_profile.client_name_ar if language == Language.ARABIC else client_profile.client_name_en
        if not client_name:
            client_name = client_profile.client_name

        frameworks_str = ", ".join([f.value for f in frameworks])

        # Extract relevant knowledge from context
        relevant_controls = []
        if context.get("structured_context"):
            for fw in frameworks:
                fw_controls = context["structured_context"].get("controls", {}).get(fw.value, [])
                relevant_controls.extend(fw_controls)

        controls_text = ""
        if relevant_controls:
            controls_text = "\n\nRelevant Controls:\n" + "\n".join([
                f"- {ctrl.get('id', '')}: {ctrl.get('text', '')[:200]}"
                for ctrl in relevant_controls[:5]
            ])

        prompt = f"""
Write a {section_title} section for an Information Security Policy document.

Client: {client_name}
Industry: {client_profile.industry}
Frameworks: {frameworks_str}
Language: {lang_name}
Section Type: {section_type}

Requirements:
1. Write in professional {lang_name} language
2. Follow Big4 consulting style and structure
3. Include references to relevant framework controls (e.g., [NCA-ECC-5-1-1], [ISO27001:5.1])
4. Be specific and actionable
5. Keep paragraphs clear and concise
6. Use proper {lang_name} formatting and terminology
{controls_text}

Write the section content now:
"""

        return prompt

    def _get_system_prompt(self, language: Language) -> str:
        """
        Get system prompt for LLM.

        Args:
            language: Target language

        Returns:
            System prompt
        """
        if language == Language.ARABIC:
            return """أنت خبير في أمن المعلومات والامتثال. مهمتك كتابة وثائق السياسات والإجراءات بأسلوب احترافي يتبع معايير شركات المحاسبة الأربع الكبرى (Big4).

المتطلبات:
- اكتب بلغة عربية فصحى احترافية
- اتبع أفضل الممارسات العالمية
- أضف مراجع للضوابط ذات الصلة
- كن دقيقاً ومحدداً
- استخدم هيكل منظم وواضح"""
        else:
            return """You are an information security and compliance expert. Your task is to write policy and procedure documents in a professional style following Big4 consulting standards.

Requirements:
- Write in professional English
- Follow global best practices
- Add references to relevant controls
- Be specific and actionable
- Use clear and organized structure"""

    def _extract_references(
        self,
        content: str,
        frameworks: List[Framework]
    ) -> List[str]:
        """
        Extract control references from content.

        Args:
            content: Generated content
            frameworks: Frameworks

        Returns:
            List of control references
        """
        import re

        references = []

        # Extract references like [NCA-ECC-5-1-1], [ISO27001:5.1], etc.
        patterns = [
            r"\[(ECC|CCC|DCC)-[\d-]+\]",
            r"\[ISO\d+:[\d.]+\]",
            r"\[(PDPL|SAMA|NIS2)-[\d.]+\]",
        ]

        for pattern in patterns:
            matches = re.findall(pattern, content)
            references.extend(matches)

        # Remove duplicates and brackets
        references = list(set([ref.strip("[]") for ref in references]))

        return references
