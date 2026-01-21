# HexaGen GRC - Offline Multi-Agent Security Consultant

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

**HexaGen GRC** is an offline, locally-running Multi-Agent system designed to help GRC professionals generate compliance documents, perform gap analyses, create risk assessments, and produce Big4-style deliverables—all without sending sensitive client data to external APIs.

## Features

- **🔒 Fully Offline**: All processing happens locally using Ollama LLM
- **🤖 Multi-Agent Architecture**: Specialized agents for different GRC tasks
- **📚 Excel-First Knowledge Base**: Parse controls, requirements, and mappings from Excel files
- **📝 Big4-Style Document Generation**: Generate policies, procedures, standards in DOCX format
- **🌐 Bilingual Support**: Full Arabic and English support with RTL formatting
- **🔍 RAG-Powered**: Semantic search with local vector database (ChromaDB)
- **🏗️ Framework Support**: NCA ECC/CCC/DCC, ISO 27001/31000, PDPL, SAMA, NIS2, and more

## Architecture

```
┌─────────────────┐
│  Eigent UI      │ (Optional - Chat Interface)
│  localhost:3001 │
└────────┬────────┘
         │ HTTP
┌────────▼────────┐
│  HexaGen Engine │
│  FastAPI Server │
│  localhost:7010 │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
┌───▼──┐  ┌──▼────┐
│Agents│  │  KB   │
│System│  │ RAG   │
└──────┘  └───┬───┘
              │
         ┌────▼────┐
         │ Ollama  │
         │ LLM     │
         │ :11434  │
         └─────────┘
```

## System Requirements

### Minimum Requirements
- **OS**: Windows 10/11, Linux, macOS
- **CPU**: Intel i7 Gen 10 or better
- **RAM**: 16GB (8GB for Ollama, 8GB for system)
- **Storage**: 20GB free space (for models and data)
- **GPU**: Optional (Intel Iris, NVIDIA, AMD) - improves performance

### Recommended for Best Performance
- **CPU**: Intel i7 Gen 13 or better
- **RAM**: 32GB
- **GPU**: NVIDIA RTX 3060+ or equivalent

## Installation (Windows)

### 1. Install Prerequisites

#### A. Install Python 3.10+
1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run installer and check "Add Python to PATH"
3. Verify installation:
```bash
python --version
```

#### B. Install Ollama
1. Download Ollama for Windows from [ollama.ai](https://ollama.ai/download)
2. Run the installer
3. Verify installation:
```bash
ollama --version
```

4. Pull a model (recommended: Mistral 7B):
```bash
ollama pull mistral:7b-instruct-q4_K_M
```

For Arabic support, also try:
```bash
ollama pull llama2:7b
ollama pull codellama:7b
```

#### C. Install Git
1. Download from [git-scm.com](https://git-scm.com/download/win)
2. Run installer with default settings

#### D. Install Docker Desktop (Optional)
1. Download from [docker.com](https://www.docker.com/products/docker-desktop)
2. Install and start Docker Desktop

### 2. Clone the Repository

```bash
git clone https://github.com/yourusername/hexagen-grc-offline.git
cd hexagen-grc-offline
```

### 3. Set Up Python Environment

#### Using Poetry (Recommended)

```bash
# Install Poetry
pip install poetry

# Install dependencies
poetry install

# Activate virtual environment
poetry shell
```

#### Using pip + venv

```bash
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -e .
```

### 4. Configure Environment

```bash
# Copy example configuration
copy .env.example .env

# Edit .env with your settings
notepad .env
```

Key settings to configure:
```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral:7b-instruct-q4_K_M
DEFAULT_LANGUAGE=ar
```

### 5. Initialize HexaGen GRC

```bash
# Initialize directories and setup
hexagen init
```

This creates:
- `data/clients/` - Client data storage
- `data/kb/` - Knowledge base storage
- `templates/` - Document templates
- `frameworks/` - Framework controls and requirements

## Quick Start

### 1. Start the API Server

```bash
hexagen serve
```

The API will be available at:
- API: http://localhost:7010
- Docs: http://localhost:7010/docs
- Health: http://localhost:7010/health

### 2. Ingest Knowledge Base

```bash
# Ingest NCA ECC controls
hexagen ingest NCA_ECC frameworks/NCA/ECC/sample_controls.csv --file-type excel --language ar

# Check ingestion status
hexagen stats
```

### 3. Search Knowledge Base

```bash
# Search in Arabic
hexagen search "سياسة أمن المعلومات" --framework NCA_ECC --language ar

# Search in English
hexagen search "access control" --framework NCA_ECC --language en
```

### 4. Generate Documents (via API)

```python
import httpx

# Create GRC task request
request = {
    "task_type": "policy",
    "client_profile": {
        "client_id": "client001",
        "client_name": "ACME Corporation",
        "client_name_ar": "شركة أكمي",
        "industry": "Financial Services",
        "classification": "Internal"
    },
    "frameworks": ["NCA_ECC", "ISO_27001"],
    "language": "ar",
    "output_type": "policy",
    "parameters": {
        "policy_type": "information_security"
    }
}

# Submit task
response = httpx.post("http://localhost:7010/api/v1/grc/task", json=request)
result = response.json()

print(f"Task ID: {result['task_id']}")
print(f"Status: {result['status']}")
```

## Project Structure

```
hexagen-grc-offline/
├── src/hexagen_grc/
│   ├── api/              # FastAPI application
│   │   ├── main.py
│   │   └── routes.py
│   ├── agents/           # Multi-agent system
│   │   ├── base.py
│   │   ├── orchestrator.py
│   │   ├── knowledge.py
│   │   ├── policy.py
│   │   ├── document.py
│   │   └── qa.py
│   ├── kb/               # Knowledge base
│   │   ├── vector_store.py
│   │   └── search.py
│   ├── ingestion/        # Data ingestion
│   │   ├── excel_parser.py
│   │   └── ingestion_service.py
│   ├── docs/             # Document generation
│   │   └── generator.py
│   ├── common/           # Shared utilities
│   │   ├── config.py
│   │   ├── schemas.py
│   │   ├── logging.py
│   │   └── utils.py
│   └── cli.py            # CLI tool
├── templates/            # DOCX templates
│   ├── policies/
│   ├── procedures/
│   └── standards/
├── frameworks/           # Framework data
│   ├── NCA/ECC/
│   ├── ISO/27001/
│   └── PDPL/
├── data/
│   ├── clients/         # Client data (gitignored)
│   └── kb/              # Knowledge base (gitignored)
├── tests/               # Unit and integration tests
├── docker-compose.yml   # Docker setup
├── Dockerfile
├── pyproject.toml       # Python dependencies
└── README.md
```

## Multi-Agent System

HexaGen uses a specialized multi-agent architecture:

### Phase 1 Agents (MVP)

1. **OrchestratorAgent**: Routes tasks to appropriate agents
2. **KnowledgeAgent**: RAG-based retrieval from vector DB
3. **PolicyAgent**: Generates policy content with LLM
4. **ProcedureAgent**: Generates procedures and SOPs
5. **DocumentAgent**: Creates DOCX files from templates
6. **QAAgent**: Quality assurance and compliance checking

### Phase 2 Agents (Future)

- **RiskAgent**: Risk assessments and registers
- **GapAgent**: Gap analysis and remediation plans
- **EvidenceAgent**: Evidence request packs
- **StrategyAgent**: SWOT and strategic roadmaps
- **VisioAgent**: Flowchart generation (Windows COM)

## Supported Frameworks

- **NCA ECC** (National Cybersecurity Authority - Essential Cybersecurity Controls)
- **NCA CCC** (Cloud Cybersecurity Controls)
- **NCA DCC** (Data Cybersecurity Controls)
- **ISO 27001** (Information Security Management)
- **ISO 31000** (Risk Management)
- **PDPL** (Personal Data Protection Law - Saudi Arabia)
- **NDMO** (National Data Management Office)
- **NIS2** (Network and Information Security Directive)
- **CST CRF** (Cybersecurity Threat Classification and Reference Framework)
- **SAMA** (Saudi Arabian Monetary Authority)

## CLI Commands

```bash
# Initialize
hexagen init

# Start server
hexagen serve

# Ingest knowledge
hexagen ingest <FRAMEWORK> <FILE_PATH> [OPTIONS]

# Search
hexagen search <QUERY> [OPTIONS]

# Show statistics
hexagen stats

# Show version
hexagen version
```

## API Endpoints

### Health Check
```
GET /health
```

### GRC Task Execution
```
POST /api/v1/grc/task
{
  "task_type": "policy",
  "client_profile": {...},
  "frameworks": ["NCA_ECC"],
  "language": "ar",
  "output_type": "policy"
}
```

### Knowledge Base Ingestion
```
POST /api/v1/kb/ingest
{
  "framework": "NCA_ECC",
  "file_path": "path/to/file.xlsx",
  "file_type": "excel"
}
```

### Knowledge Base Search
```
POST /api/v1/kb/search
{
  "query": "access control",
  "frameworks": ["NCA_ECC"],
  "top_k": 10
}
```

## Troubleshooting

### Ollama Connection Error
```
Error: Could not connect to Ollama
```
**Solution**: Ensure Ollama is running:
```bash
ollama serve
```

### Out of Memory
```
Error: Out of memory
```
**Solution**: Use a smaller quantized model:
```bash
ollama pull mistral:7b-instruct-q4_0
```

### Arabic Text Issues
```
Issue: Arabic text not displaying correctly
```
**Solution**: Ensure you're using Arabic-capable fonts in templates and set RTL in document properties.

## Performance Optimization

### For 16GB RAM Systems
- Use Q4_K_M or Q4_0 quantized models
- Limit concurrent agent execution
- Set `KB_CHUNK_SIZE=256` in .env

### For 32GB+ RAM Systems
- Use Q5_K_M or higher quantized models
- Enable parallel agent execution
- Increase `RAG_TOP_K=20` for better context

## License

This project is licensed under the MIT License - see LICENSE file for details.

---

**Built with ❤️ for GRC Professionals**