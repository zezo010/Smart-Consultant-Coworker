"""Configuration management for HexaGen GRC."""

import os
from pathlib import Path
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # Server Settings
    host: str = "0.0.0.0"
    port: int = 7010
    log_level: str = "INFO"
    debug: bool = False
    reload: bool = True

    # Ollama Settings (Local LLM)
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "mistral:7b-instruct-q4_K_M"

    # Embeddings Settings (Local)
    embedding_model: str = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"

    # Vector Database Settings
    chroma_persist_dir: str = "./data/kb/vectordb"
    chroma_host: str = "localhost"
    chroma_port: int = 8000
    use_local_chroma: bool = True

    # Knowledge Base Settings
    kb_staging_dir: str = "./data/kb/staging"
    kb_processed_dir: str = "./data/kb/processed"
    kb_chunk_size: int = 512
    kb_chunk_overlap: int = 50

    # Templates Settings
    templates_dir: str = "./templates"
    frameworks_dir: str = "./frameworks"

    # Client Data Settings
    clients_data_dir: str = "./data/clients"

    # Agent Settings
    max_agent_iterations: int = 5
    agent_temperature: float = 0.3
    agent_max_tokens: int = 2048

    # Document Generation Settings
    default_language: str = "ar"
    supported_languages: List[str] = ["ar", "en"]
    output_format: str = "docx"

    # RAG Settings
    rag_top_k: int = 10
    rag_similarity_threshold: float = 0.7

    # Rate Limiting
    rate_limit_enabled: bool = False
    max_requests_per_minute: int = 60

    # Security
    api_key_enabled: bool = False
    api_key: str = "your-secret-key-here"

    @property
    def base_dir(self) -> Path:
        """Get the base directory of the project."""
        return Path(__file__).parent.parent.parent.parent

    @property
    def templates_path(self) -> Path:
        """Get templates directory path."""
        return self.base_dir / self.templates_dir

    @property
    def frameworks_path(self) -> Path:
        """Get frameworks directory path."""
        return self.base_dir / self.frameworks_dir

    @property
    def clients_path(self) -> Path:
        """Get clients data directory path."""
        return self.base_dir / self.clients_data_dir

    @property
    def kb_staging_path(self) -> Path:
        """Get KB staging directory path."""
        return self.base_dir / self.kb_staging_dir

    @property
    def kb_processed_path(self) -> Path:
        """Get KB processed directory path."""
        return self.base_dir / self.kb_processed_dir

    @property
    def chroma_path(self) -> Path:
        """Get Chroma persist directory path."""
        return self.base_dir / self.chroma_persist_dir

    def ensure_directories(self) -> None:
        """Create necessary directories if they don't exist."""
        directories = [
            self.templates_path,
            self.frameworks_path,
            self.clients_path,
            self.kb_staging_path,
            self.kb_processed_path,
            self.chroma_path,
        ]
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)


# Global settings instance
settings = Settings()
