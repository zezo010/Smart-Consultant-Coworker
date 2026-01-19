"""Search service for knowledge base."""

from typing import Any, Dict, List, Optional

from ..common.logging import get_logger
from ..common.schemas import Framework, Language, SearchQuery, SearchResult, KnowledgeChunk
from .vector_store import VectorStore

logger = get_logger(__name__)


class SearchService:
    """
    Search service for querying knowledge base.

    Provides high-level search interface over vector store.
    """

    def __init__(self, vector_store: VectorStore):
        """
        Initialize search service.

        Args:
            vector_store: Vector store instance
        """
        self.vector_store = vector_store

    async def search(self, query: SearchQuery) -> List[SearchResult]:
        """
        Search knowledge base.

        Args:
            query: Search query

        Returns:
            List of search results
        """
        logger.info(f"Searching: {query.query[:100]}...")

        # Determine framework(s) to search
        frameworks = query.frameworks if query.frameworks else None
        framework = frameworks[0] if frameworks and len(frameworks) == 1 else None

        # Execute search
        raw_results = await self.vector_store.search(
            query=query.query,
            framework=framework,
            language=query.language,
            top_k=query.top_k,
            filters=query.filters
        )

        # Convert to SearchResult objects
        results = []
        for raw in raw_results:
            chunk = KnowledgeChunk(
                chunk_id=raw["id"],
                framework=Framework(raw["metadata"].get("framework", "NCA_ECC")),
                type=raw["metadata"].get("type", ""),
                id=raw["metadata"].get("id", ""),
                lang=Language(raw["metadata"].get("lang", "ar")),
                text=raw["text"],
                metadata=raw["metadata"]
            )

            results.append(SearchResult(
                chunk=chunk,
                score=raw["score"],
                source=raw["metadata"].get("source", "")
            ))

        logger.info(f"Found {len(results)} results")

        return results

    async def search_by_control_id(
        self,
        control_id: str,
        framework: Framework,
        language: Optional[Language] = None
    ) -> Optional[SearchResult]:
        """
        Search for a specific control by ID.

        Args:
            control_id: Control identifier
            framework: Framework name
            language: Optional language filter

        Returns:
            Search result or None
        """
        query = SearchQuery(
            query=control_id,
            frameworks=[framework],
            language=language,
            top_k=1,
            filters={"type": "control", "id": control_id}
        )

        results = await self.search(query)

        return results[0] if results else None

    async def search_by_type(
        self,
        chunk_type: str,
        framework: Framework,
        language: Optional[Language] = None,
        top_k: int = 10
    ) -> List[SearchResult]:
        """
        Search by chunk type (control, requirement, evidence, etc.).

        Args:
            chunk_type: Type of chunk
            framework: Framework name
            language: Optional language filter
            top_k: Number of results

        Returns:
            List of search results
        """
        # Use a generic query and filter by type
        query = SearchQuery(
            query=chunk_type,
            frameworks=[framework],
            language=language,
            top_k=top_k,
            filters={"type": chunk_type}
        )

        results = await self.search(query)

        return results

    async def semantic_search(
        self,
        query: str,
        frameworks: List[Framework],
        language: Language,
        top_k: int = 10
    ) -> List[SearchResult]:
        """
        Perform semantic search across frameworks.

        Args:
            query: Search query
            frameworks: List of frameworks to search
            language: Language preference
            top_k: Number of results

        Returns:
            List of search results
        """
        search_query = SearchQuery(
            query=query,
            frameworks=frameworks,
            language=language,
            top_k=top_k
        )

        return await self.search(search_query)
