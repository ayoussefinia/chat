FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies (if needed, e.g., psycopg2)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev curl \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install uv and dependencies (no bash process substitution)
RUN pip install --upgrade pip \
    && pip install uv \
    && uv pip install --system --no-cache .

# Copy rest of backend code
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Run FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
