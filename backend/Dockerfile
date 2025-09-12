FROM python:3.13-alpine

# Set working directory
WORKDIR /app

# Install system dependencies (alpine)
RUN apk add --no-cache build-base postgresql-dev curl

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install uv and dependencies
RUN pip install --upgrade pip \
    && pip install uv \
    && uv pip install --system --no-cache .

# Copy rest of backend code
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Run FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
