# Multi-stage build for ML Pipeline Application
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH="/app/src" \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd --create-home --shell /bin/bash mluser

# Set working directory
WORKDIR /app

# Copy requirements first (for better caching)
COPY requirements.txt pyproject.toml ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY config/ ./config/
COPY templates/ ./templates/
COPY static/ ./static/
COPY app.py main.py ./

# Create necessary directories
RUN mkdir -p logs artifacts/model_trainer artifacts/data_transformation

# Change ownership to mluser
RUN chown -R mluser:mluser /app

# Switch to non-root user
USER mluser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Expose ports
EXPOSE 5000 8000

# Default command
CMD ["python", "app.py"]

# Production stage
FROM base as production

# Copy any additional production configs
COPY start_observability.sh ./
RUN chmod +x start_observability.sh

# Production-specific optimizations
ENV FLASK_ENV=production \
    FLASK_DEBUG=0

# Observability stage (includes monitoring tools)
FROM base as observability

# Install additional monitoring dependencies
USER root
RUN pip install prometheus-client jaeger-client opentelemetry-api

# Copy observability configs
COPY observability/ ./observability/

USER mluser

# Command for observability-enabled container
CMD ["sh", "-c", "python app.py & sleep 10 && python -c 'from src.mlpipeline.observability.metrics import pipeline_metrics; pipeline_metrics.start_metrics_server(8000)' && wait"]
