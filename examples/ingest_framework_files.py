"""
Example: Ingest Framework Files (Controls, Requirements, Gap Assessments)

This example shows how to ingest multiple types of framework files:
- Controls Excel files
- Requirements Excel files
- Gap assessment files
- Evidence catalogs
- Mapping files
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from hexagen_grc.common.schemas import Framework, Language, IngestionRequest
from hexagen_grc.kb.vector_store import VectorStore
from hexagen_grc.ingestion.ingestion_service import IngestionService


async def ingest_all_framework_files():
    """Ingest all framework files."""

    print("=" * 70)
    print("HexaGen GRC - Framework Files Ingestion")
    print("=" * 70)
    print()

    # Initialize services
    print("📦 Initializing services...")
    vector_store = VectorStore()
    await vector_store.initialize()
    ingestion_service = IngestionService(vector_store)
    print("   ✓ Services initialized")
    print()

    # Define base path
    base_path = Path("frameworks/NCA/ECC")

    # Files to ingest
    files_to_ingest = [
        {
            "path": base_path / "source_excel" / "NCA_ECC_Controls_AR.xlsx",
            "type": "controls",
            "language": Language.ARABIC,
            "description": "NCA ECC Controls (Arabic)"
        },
        {
            "path": base_path / "requirements" / "all_requirements.xlsx",
            "type": "requirements",
            "language": Language.ARABIC,
            "description": "Detailed Requirements"
        },
        {
            "path": base_path / "gap_assessments" / "gap_template.xlsx",
            "type": "gap_assessment",
            "language": Language.ARABIC,
            "description": "Gap Assessment Template"
        },
        {
            "path": base_path / "evidence_catalog" / "evidence_by_control.xlsx",
            "type": "evidence",
            "language": Language.ARABIC,
            "description": "Evidence Catalog"
        },
        {
            "path": base_path / "mappings" / "ECC_to_ISO27001.xlsx",
            "type": "mapping",
            "language": Language.ENGLISH,
            "description": "ECC to ISO 27001 Mapping"
        }
    ]

    # Ingest each file
    total_chunks = 0
    successful = 0
    failed = 0

    for i, file_info in enumerate(files_to_ingest, 1):
        print(f"[{i}/{len(files_to_ingest)}] {file_info['description']}")
        print(f"    Path: {file_info['path']}")

        # Check if file exists
        if not file_info['path'].exists():
            print(f"    ⚠️  File not found - Skipping")
            print()
            failed += 1
            continue

        # Create ingestion request
        request = IngestionRequest(
            framework=Framework.NCA_ECC,
            file_path=str(file_info['path']),
            file_type="excel",
            language=file_info['language'],
            metadata={
                "type": file_info['type'],
                "description": file_info['description']
            }
        )

        # Ingest
        try:
            result = await ingestion_service.ingest_file(request)

            if result.status == "success":
                print(f"    ✓ Success: {result.chunks_created} chunks created")
                total_chunks += result.chunks_created
                successful += 1
            else:
                print(f"    ✗ Failed: {', '.join(result.errors)}")
                failed += 1

        except Exception as e:
            print(f"    ✗ Error: {e}")
            failed += 1

        print()

    # Summary
    print("=" * 70)
    print("📊 Ingestion Summary")
    print("=" * 70)
    print(f"Total Files Processed: {len(files_to_ingest)}")
    print(f"✓ Successful: {successful}")
    print(f"✗ Failed: {failed}")
    print(f"📦 Total Chunks Created: {total_chunks}")
    print()

    # Show KB stats
    print("📈 Knowledge Base Statistics")
    print("-" * 70)
    stats = await vector_store.get_stats()
    for framework, count in stats['frameworks'].items():
        print(f"  {framework}: {count} chunks")
    print(f"\n  Total: {stats['total_chunks']} chunks")
    print()

    print("=" * 70)
    print("✅ Ingestion Complete!")
    print("=" * 70)


async def ingest_directory(directory_path: str, framework: Framework):
    """
    Ingest all Excel files in a directory.

    Args:
        directory_path: Path to directory
        framework: Framework name
    """
    print(f"\n📂 Ingesting directory: {directory_path}")
    print("-" * 70)

    # Initialize
    vector_store = VectorStore()
    await vector_store.initialize()
    ingestion_service = IngestionService(vector_store)

    # Find all Excel files
    dir_path = Path(directory_path)
    excel_files = list(dir_path.glob("*.xlsx")) + list(dir_path.glob("*.xls"))

    print(f"Found {len(excel_files)} Excel files")
    print()

    # Ingest each file
    for excel_file in excel_files:
        print(f"  Processing: {excel_file.name}")

        request = IngestionRequest(
            framework=framework,
            file_path=str(excel_file),
            file_type="excel",
            language=Language.ARABIC
        )

        result = await ingestion_service.ingest_file(request)

        if result.status == "success":
            print(f"    ✓ {result.chunks_created} chunks")
        else:
            print(f"    ✗ Failed")

    print()


async def ingest_client_gap_assessment(client_id: str, gap_file_path: str):
    """
    Ingest client-specific gap assessment.

    Args:
        client_id: Client ID
        gap_file_path: Path to gap assessment file
    """
    print(f"\n📊 Ingesting Gap Assessment for Client: {client_id}")
    print("-" * 70)

    # Initialize
    vector_store = VectorStore()
    await vector_store.initialize()
    ingestion_service = IngestionService(vector_store)

    # Ingest
    request = IngestionRequest(
        framework=Framework.NCA_ECC,
        file_path=gap_file_path,
        file_type="excel",
        language=Language.ARABIC,
        metadata={
            "type": "gap_assessment",
            "client_id": client_id
        }
    )

    result = await ingestion_service.ingest_file(request)

    if result.status == "success":
        print(f"✓ Gap assessment ingested: {result.chunks_created} findings")
    else:
        print(f"✗ Failed: {', '.join(result.errors)}")

    print()


def main():
    """Main function."""
    import argparse

    parser = argparse.ArgumentParser(description="Ingest framework files")
    parser.add_argument(
        "--mode",
        choices=["all", "directory", "gap"],
        default="all",
        help="Ingestion mode"
    )
    parser.add_argument("--path", help="Path to file or directory")
    parser.add_argument("--client-id", help="Client ID (for gap assessment)")

    args = parser.parse_args()

    if args.mode == "all":
        asyncio.run(ingest_all_framework_files())
    elif args.mode == "directory" and args.path:
        asyncio.run(ingest_directory(args.path, Framework.NCA_ECC))
    elif args.mode == "gap" and args.path and args.client_id:
        asyncio.run(ingest_client_gap_assessment(args.client_id, args.path))
    else:
        print("Invalid arguments. Use --help for usage information.")


if __name__ == "__main__":
    main()
