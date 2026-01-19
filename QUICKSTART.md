# HexaGen GRC - Quick Start Guide

This guide will help you get HexaGen GRC up and running in under 10 minutes.

## Prerequisites Checklist

Before starting, ensure you have:

- [ ] Windows 10/11, Linux, or macOS
- [ ] 16GB+ RAM
- [ ] 20GB+ free disk space
- [ ] Internet connection (for initial setup only)

## Step 1: Install Prerequisites (5 minutes)

### Python 3.10+

```bash
# Download from python.org or use:
# Windows: winget install Python.Python.3.11
# Mac: brew install python@3.11
# Ubuntu: sudo apt install python3.11

# Verify:
python --version
```

### Ollama

```bash
# Download and install from ollama.ai

# Verify:
ollama --version

# Pull model:
ollama pull mistral:7b-instruct-q4_K_M
```

## Step 2: Setup HexaGen (3 minutes)

```bash
# Clone repository
git clone https://github.com/yourusername/hexagen-grc-offline.git
cd hexagen-grc-offline

# Windows users: Run setup script
setup_windows.bat

# Or manual setup:
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

pip install poetry
poetry install
```

## Step 3: Configure (1 minute)

```bash
# Copy example config
cp .env.example .env

# Edit if needed (default settings work for most users)
notepad .env  # Windows
# nano .env  # Linux/Mac
```

## Step 4: Initialize (1 minute)

```bash
# Activate environment if not already active
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Initialize
hexagen init
```

## Step 5: Start Server (30 seconds)

```bash
hexagen serve
```

Server will start at: http://localhost:7010

API Docs: http://localhost:7010/docs

## Step 6: Ingest Sample Data (Optional)

```bash
# In a new terminal (keep server running)
hexagen ingest NCA_ECC frameworks/NCA/ECC/sample_controls.csv --file-type excel --language ar

# Check stats
hexagen stats
```

## Step 7: Test It Out

### Via CLI:

```bash
hexagen search "access control" --framework NCA_ECC --language en
```

### Via Python:

```python
import httpx

response = httpx.get("http://localhost:7010/health")
print(response.json())
```

### Via Browser:

Open http://localhost:7010/docs and try the interactive API!

## What's Next?

### Add Your Own Data

1. Prepare Excel files with controls (see `frameworks/NCA/ECC/sample_controls.csv` for format)
2. Ingest: `hexagen ingest <FRAMEWORK> <FILE_PATH>`
3. Search and generate documents!

### Generate Your First Policy

```python
import httpx

request = {
    "task_type": "policy",
    "client_profile": {
        "client_id": "client001",
        "client_name": "My Company",
        "industry": "Technology",
        "classification": "Internal"
    },
    "frameworks": ["NCA_ECC"],
    "language": "ar",
    "output_type": "policy"
}

response = httpx.post("http://localhost:7010/api/v1/grc/task", json=request)
print(response.json())
```

### Integrate with Eigent

1. Start HexaGen: `hexagen serve`
2. Configure Eigent provider to point to `http://localhost:7010`
3. Chat with GRC agents through Eigent UI!

## Troubleshooting

### Ollama Not Responding

```bash
# Start Ollama manually
ollama serve
```

### Port Already in Use

```bash
# Use different port
hexagen serve --port 7011
```

### Out of Memory

```bash
# Use smaller model
ollama pull mistral:7b-instruct-q4_0
```

## Need Help?

- Documentation: See `README.md`
- Issues: GitHub Issues
- Examples: Check `examples/` directory

## Success!

You now have a fully functional offline GRC consultant running on your machine! 🎉

---

**Estimated Total Time: ~10 minutes**
