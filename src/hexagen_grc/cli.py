"""CLI tool for HexaGen GRC."""

import asyncio
import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from .common.config import settings
from .common.logging import setup_logging
from .common.schemas import (
    ClientProfile,
    Framework,
    GRCTaskRequest,
    IngestionRequest,
    Language,
    TaskType,
    DocumentType,
)
from .kb.vector_store import VectorStore
from .ingestion.ingestion_service import IngestionService

app = typer.Typer(help="HexaGen GRC - Offline Multi-Agent Security Consultant")
console = Console()

# Setup logging
logger = setup_logging()


@app.command()
def ingest(
    framework: str = typer.Argument(..., help="Framework name (e.g., NCA_ECC)"),
    file_path: str = typer.Argument(..., help="Path to file to ingest"),
    file_type: str = typer.Option("excel", help="File type (excel, pdf, docx)"),
    language: str = typer.Option("ar", help="Language (ar, en)"),
) -> None:
    """Ingest knowledge base files."""
    console.print(f"[bold blue]Ingesting knowledge base...[/bold blue]")

    async def run_ingest():
        # Initialize vector store
        vector_store = VectorStore()
        await vector_store.initialize()

        # Initialize ingestion service
        ingestion_service = IngestionService(vector_store)

        # Create request
        request = IngestionRequest(
            framework=Framework(framework),
            file_path=file_path,
            file_type=file_type,
            language=Language(language) if language else None,
        )

        # Ingest file
        result = await ingestion_service.ingest_file(request)

        # Display results
        if result.status == "success":
            console.print(f"[green]✓[/green] Successfully ingested {result.chunks_created} chunks")
        else:
            console.print(f"[red]✗[/red] Ingestion failed:")
            for error in result.errors:
                console.print(f"  - {error}")

    asyncio.run(run_ingest())


@app.command()
def search(
    query: str = typer.Argument(..., help="Search query"),
    framework: Optional[str] = typer.Option(None, help="Framework to search"),
    language: str = typer.Option("ar", help="Language (ar, en)"),
    top_k: int = typer.Option(5, help="Number of results"),
) -> None:
    """Search knowledge base."""
    console.print(f"[bold blue]Searching knowledge base...[/bold blue]")

    async def run_search():
        # Initialize vector store
        vector_store = VectorStore()
        await vector_store.initialize()

        # Search
        results = await vector_store.search(
            query=query,
            framework=Framework(framework) if framework else None,
            language=Language(language) if language else None,
            top_k=top_k,
        )

        # Display results
        if results:
            table = Table(title=f"Search Results ({len(results)})")
            table.add_column("Score", style="cyan")
            table.add_column("Framework", style="magenta")
            table.add_column("ID", style="yellow")
            table.add_column("Text", style="white")

            for result in results:
                table.add_row(
                    f"{result['score']:.2f}",
                    result["metadata"].get("framework", ""),
                    result["metadata"].get("id", ""),
                    result["text"][:100] + "...",
                )

            console.print(table)
        else:
            console.print("[yellow]No results found[/yellow]")

    asyncio.run(run_search())


@app.command()
def stats() -> None:
    """Show knowledge base statistics."""
    console.print(f"[bold blue]Knowledge Base Statistics[/bold blue]")

    async def run_stats():
        # Initialize vector store
        vector_store = VectorStore()
        await vector_store.initialize()

        # Get stats
        stats = await vector_store.get_stats()

        # Display stats
        table = Table(title="Knowledge Base Stats")
        table.add_column("Framework", style="cyan")
        table.add_column("Chunks", style="green")

        for framework, count in stats["frameworks"].items():
            table.add_row(framework, str(count))

        table.add_row("", "")
        table.add_row("[bold]Total[/bold]", f"[bold]{stats['total_chunks']}[/bold]")

        console.print(table)

    asyncio.run(run_stats())


@app.command()
def init() -> None:
    """Initialize HexaGen GRC (create directories, etc.)."""
    console.print("[bold blue]Initializing HexaGen GRC...[/bold blue]")

    # Create directories
    settings.ensure_directories()

    console.print("[green]✓[/green] Directories created")
    console.print(f"  - Templates: {settings.templates_path}")
    console.print(f"  - Frameworks: {settings.frameworks_path}")
    console.print(f"  - Clients: {settings.clients_path}")
    console.print(f"  - Knowledge Base: {settings.chroma_path}")

    console.print("\n[bold green]HexaGen GRC initialized successfully![/bold green]")


@app.command()
def serve(
    host: str = typer.Option("0.0.0.0", help="Host to bind"),
    port: int = typer.Option(7010, help="Port to bind"),
    reload: bool = typer.Option(False, help="Enable auto-reload"),
) -> None:
    """Start the HexaGen GRC API server."""
    import uvicorn

    console.print(f"[bold blue]Starting HexaGen GRC Engine...[/bold blue]")
    console.print(f"  - Host: {host}")
    console.print(f"  - Port: {port}")
    console.print(f"  - Reload: {reload}")
    console.print(f"\n[bold green]API Documentation:[/bold green] http://{host}:{port}/docs\n")

    uvicorn.run(
        "hexagen_grc.api.main:app",
        host=host,
        port=port,
        reload=reload,
        log_level=settings.log_level.lower(),
    )


@app.command()
def version() -> None:
    """Show version information."""
    from . import __version__

    console.print(f"[bold]HexaGen GRC[/bold] version [cyan]{__version__}[/cyan]")


def main() -> None:
    """Main entry point."""
    app()


if __name__ == "__main__":
    main()
