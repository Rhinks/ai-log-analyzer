FROM python:3.12-slim

WORKDIR /app

# Copy uv binary from official uv image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy dependency files first (for caching)
COPY pyproject.toml uv.lock ./

# Install dependencies to venv
RUN uv sync --frozen --no-dev

# Copy rest of the code
COPY . .

# Set path to venv
ENV PATH="/app/.venv/bin:$PATH"

# Expose port
EXPOSE 8000

# Start FastAPI
CMD ["uvicorn", "app.api.routes:app", "--host", "0.0.0.0", "--port", "8000"]
