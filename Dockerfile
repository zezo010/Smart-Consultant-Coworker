FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY pyproject.toml poetry.lock* ./

# Install poetry and dependencies
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

# Copy application code
COPY src/ ./src/
COPY templates/ ./templates/
COPY frameworks/ ./frameworks/

# Create data directories
RUN mkdir -p /app/data/clients /app/data/kb/staging /app/data/kb/processed /app/data/kb/vectordb

# Expose port
EXPOSE 7010

# Run the application
CMD ["uvicorn", "hexagen_grc.api.main:app", "--host", "0.0.0.0", "--port", "7010", "--reload"]
