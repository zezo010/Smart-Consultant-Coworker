"""Vector store for knowledge base."""

from pathlib import Path
from typing import Any, Dict, List, Optional

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

from ..common.config import settings
from ..common.logging import get_logger
from ..common.schemas import Framework, KnowledgeChunk, Language

logger = get_logger(__name__)


class VectorStore:
    """
    Vector store for storing and retrieving knowledge chunks.

    Uses ChromaDB for local vector storage and sentence-transformers for embeddings.
    """

    def __init__(self):
        """Initialize vector store."""
        self.chroma_client = None
        self.embedding_model = None
        self.collections = {}

    async def initialize(self) -> None:
        """Initialize ChromaDB and embedding model."""
        logger.info("Initializing vector store...")

        # Initialize ChromaDB
        if settings.use_local_chroma:
            self.chroma_client = chromadb.Client(
                Settings(
                    chroma_db_impl="duckdb+parquet",
                    persist_directory=str(settings.chroma_path),
                    anonymized_telemetry=False
                )
            )
        else:
            self.chroma_client = chromadb.HttpClient(
                host=settings.chroma_host,
                port=settings.chroma_port
            )

        # Initialize embedding model
        logger.info(f"Loading embedding model: {settings.embedding_model}")
        self.embedding_model = SentenceTransformer(settings.embedding_model)

        logger.info("Vector store initialized successfully")

    def get_or_create_collection(self, framework: Framework) -> chromadb.Collection:
        """
        Get or create a collection for a framework.

        Args:
            framework: Framework name

        Returns:
            ChromaDB collection
        """
        collection_name = f"hexagen_{framework.value.lower()}"

        if collection_name not in self.collections:
            self.collections[collection_name] = self.chroma_client.get_or_create_collection(
                name=collection_name,
                metadata={"framework": framework.value}
            )

        return self.collections[collection_name]

    async def add_chunks(
        self,
        chunks: List[KnowledgeChunk],
        framework: Framework
    ) -> int:
        """
        Add knowledge chunks to vector store.

        Args:
            chunks: List of knowledge chunks
            framework: Framework name

        Returns:
            Number of chunks added
        """
        if not chunks:
            return 0

        collection = self.get_or_create_collection(framework)

        # Prepare data for ChromaDB
        ids = []
        documents = []
        metadatas = []
        embeddings = []

        for chunk in chunks:
            ids.append(chunk.chunk_id)
            documents.append(chunk.text)
            metadatas.append({
                "framework": chunk.framework.value,
                "type": chunk.type,
                "id": chunk.id,
                "lang": chunk.lang.value,
                **chunk.metadata
            })

            # Generate embedding
            embedding = self.embedding_model.encode(chunk.text).tolist()
            embeddings.append(embedding)

        # Add to collection
        collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
            embeddings=embeddings
        )

        logger.info(f"Added {len(chunks)} chunks to {framework.value}")

        return len(chunks)

    async def search(
        self,
        query: str,
        framework: Optional[Framework] = None,
        language: Optional[Language] = None,
        top_k: int = 10,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Search vector store.

        Args:
            query: Search query
            framework: Optional framework filter
            language: Optional language filter
            top_k: Number of results to return
            filters: Additional filters

        Returns:
            List of search results
        """
        # Generate query embedding
        query_embedding = self.embedding_model.encode(query).tolist()

        results = []

        # Search in framework-specific collection or all collections
        collections_to_search = []
        if framework:
            collections_to_search = [self.get_or_create_collection(framework)]
        else:
            # Search all framework collections
            for fw in Framework:
                try:
                    collections_to_search.append(self.get_or_create_collection(fw))
                except Exception as e:
                    logger.warning(f"Could not access collection for {fw.value}: {e}")

        # Build where clause
        where = {}
        if language:
            where["lang"] = language.value
        if filters:
            where.update(filters)

        # Search each collection
        for collection in collections_to_search:
            try:
                search_results = collection.query(
                    query_embeddings=[query_embedding],
                    n_results=top_k,
                    where=where if where else None
                )

                # Process results
                if search_results and search_results["ids"]:
                    for i, doc_id in enumerate(search_results["ids"][0]):
                        results.append({
                            "id": doc_id,
                            "text": search_results["documents"][0][i],
                            "metadata": search_results["metadatas"][0][i],
                            "score": 1 - search_results["distances"][0][i] if "distances" in search_results else 1.0
                        })

            except Exception as e:
                logger.error(f"Error searching collection {collection.name}: {e}")

        # Sort by score and return top_k
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]

    async def delete_collection(self, framework: Framework) -> None:
        """
        Delete a framework collection.

        Args:
            framework: Framework name
        """
        collection_name = f"hexagen_{framework.value.lower()}"

        try:
            self.chroma_client.delete_collection(name=collection_name)
            if collection_name in self.collections:
                del self.collections[collection_name]
            logger.info(f"Deleted collection: {collection_name}")
        except Exception as e:
            logger.error(f"Error deleting collection {collection_name}: {e}")

    async def get_stats(self) -> Dict[str, Any]:
        """
        Get vector store statistics.

        Returns:
            Statistics dictionary
        """
        stats = {
            "total_collections": 0,
            "total_chunks": 0,
            "frameworks": {}
        }

        for framework in Framework:
            try:
                collection = self.get_or_create_collection(framework)
                count = collection.count()
                stats["frameworks"][framework.value] = count
                stats["total_chunks"] += count
                if count > 0:
                    stats["total_collections"] += 1
            except Exception as e:
                logger.warning(f"Could not get stats for {framework.value}: {e}")

        return stats
