"""Ingestion pipeline for knowledge base."""

from .excel_parser import ExcelParser
from .ingestion_service import IngestionService

__all__ = ["ExcelParser", "IngestionService"]
