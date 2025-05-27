# Multi-stage build for smaller final image
FROM python:3.13-slim AS builder

# Install uv for fast dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

# Set environment variables for Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

# Create app directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies using uv
RUN uv sync --frozen --no-install-project --no-dev

# Production stage
FROM python:3.13-slim

# Install security updates and create non-root user
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    groupadd -r buddy && \
    useradd -r -g buddy -d /app -s /sbin/nologin buddy

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/.venv/bin:$PATH"

# Set working directory and create with proper ownership
WORKDIR /app
RUN chown buddy:buddy /app

# Copy virtual environment from builder stage
COPY --from=builder --chown=buddy:buddy /app/.venv /app/.venv

# Copy application code
COPY --chown=buddy:buddy . .

# Create logs directory and ensure the bot can write log files
RUN mkdir -p /app/logs && \
    chown -R buddy:buddy /app && \
    chmod 755 /app/logs

# Switch to non-root user
USER buddy

# Health check for the Discord bot (avoid file operations)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import discord; print('Bot dependencies OK')" || exit 1

# Run the application
CMD ["python", "main.py"]
