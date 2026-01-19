"""Data schemas and models for HexaGen GRC."""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class Language(str, Enum):
    """Supported languages."""
    ARABIC = "ar"
    ENGLISH = "en"


class TaskType(str, Enum):
    """Types of GRC tasks."""
    POLICY = "policy"
    PROCEDURE = "procedure"
    STANDARD = "standard"
    GAP_ANALYSIS = "gap_analysis"
    RISK_ASSESSMENT = "risk_assessment"
    EVIDENCE_REQUEST = "evidence_request"
    STRATEGY_PACK = "strategy_pack"
    COMPLIANCE_CHECK = "compliance_check"


class Framework(str, Enum):
    """Supported compliance frameworks."""
    NCA_ECC = "NCA_ECC"
    NCA_CCC = "NCA_CCC"
    NCA_DCC = "NCA_DCC"
    ISO_27001 = "ISO_27001"
    ISO_31000 = "ISO_31000"
    PDPL = "PDPL"
    NDMO = "NDMO"
    NIS2 = "NIS2"
    CST_CRF = "CST_CRF"
    SAMA = "SAMA"


class DocumentType(str, Enum):
    """Types of generated documents."""
    POLICY = "policy"
    PROCEDURE = "procedure"
    STANDARD = "standard"
    REPORT = "report"
    REGISTER = "register"
    PACK = "pack"


class AgentStatus(str, Enum):
    """Agent execution status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


# Request/Response Models

class ClientProfile(BaseModel):
    """Client organization profile."""
    client_id: str
    client_name: str
    client_name_ar: Optional[str] = None
    client_name_en: Optional[str] = None
    industry: str
    sector: Optional[str] = None
    organization_size: Optional[str] = None
    classification: str = "Internal"
    metadata: Dict[str, Any] = Field(default_factory=dict)


class GRCTaskRequest(BaseModel):
    """Request model for GRC task execution."""
    task_type: TaskType
    client_profile: ClientProfile
    frameworks: List[Framework]
    language: Language = Language.ARABIC
    output_type: DocumentType
    parameters: Dict[str, Any] = Field(default_factory=dict)
    template_name: Optional[str] = None


class Artifact(BaseModel):
    """Generated artifact (document, report, etc.)."""
    artifact_id: str
    name: str
    type: DocumentType
    file_path: str
    language: Language
    frameworks: List[Framework]
    created_at: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class AgentMessage(BaseModel):
    """Message from agent execution."""
    agent: str
    message: str
    level: str = "info"  # info, warning, error
    timestamp: datetime = Field(default_factory=datetime.now)


class GRCTaskResponse(BaseModel):
    """Response model for GRC task execution."""
    task_id: str
    status: AgentStatus
    task_type: TaskType
    artifacts: List[Artifact] = Field(default_factory=list)
    messages: List[AgentMessage] = Field(default_factory=list)
    execution_time: float = 0.0
    error: Optional[str] = None


# Knowledge Base Models

class KnowledgeChunk(BaseModel):
    """Knowledge base chunk."""
    chunk_id: str
    framework: Framework
    type: str  # control, requirement, evidence, tracker, mapping
    id: str  # e.g., ECC-5-1-1
    lang: Language
    text: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ControlMetadata(BaseModel):
    """Metadata for a control."""
    control_id: str
    control_title: str
    control_title_ar: Optional[str] = None
    control_title_en: Optional[str] = None
    requirements: List[str] = Field(default_factory=list)
    implementation_guidance: Optional[str] = None
    expected_evidence: List[str] = Field(default_factory=list)
    mapping: Dict[str, List[str]] = Field(default_factory=dict)


class SearchQuery(BaseModel):
    """Search query for knowledge base."""
    query: str
    frameworks: List[Framework] = Field(default_factory=list)
    language: Optional[Language] = None
    top_k: int = 10
    filters: Dict[str, Any] = Field(default_factory=dict)


class SearchResult(BaseModel):
    """Search result from knowledge base."""
    chunk: KnowledgeChunk
    score: float
    source: str


# Document Generation Models

class DocumentSection(BaseModel):
    """Document section content."""
    section_id: str
    title: str
    content: str
    subsections: List["DocumentSection"] = Field(default_factory=list)
    references: List[str] = Field(default_factory=list)


class DocumentContent(BaseModel):
    """Complete document content."""
    title: str
    version: str = "1.0"
    classification: str = "Internal"
    client: ClientProfile
    language: Language
    frameworks: List[Framework]
    sections: List[DocumentSection]
    metadata: Dict[str, Any] = Field(default_factory=dict)


class TemplateMapping(BaseModel):
    """Template variable mapping."""
    variable_name: str
    placeholder: str
    type: str  # string, date, table, list
    value: Any
    formatting: Optional[Dict[str, Any]] = None


# Ingestion Models

class IngestionRequest(BaseModel):
    """Request for knowledge base ingestion."""
    framework: Framework
    file_path: str
    file_type: str  # excel, pdf, docx
    language: Optional[Language] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class IngestionResult(BaseModel):
    """Result of knowledge base ingestion."""
    framework: Framework
    chunks_created: int
    file_processed: str
    status: str
    errors: List[str] = Field(default_factory=list)


# Health Check

class HealthCheck(BaseModel):
    """Health check response."""
    status: str = "healthy"
    version: str = "0.1.0"
    ollama_available: bool = False
    chroma_available: bool = False
    timestamp: datetime = Field(default_factory=datetime.now)
