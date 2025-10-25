# Use Python 3.11 slim image for smaller size
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files first (for better layer caching)
COPY pyproject.toml ./

# Install Python dependencies
RUN pip install --no-cache-dir -e .

# Copy the entire application
COPY . .

# Create directory for logs
RUN mkdir -p /app/logs

# Set environment variables with defaults
ENV ZERION_API_KEY="" \
    CONFIG_PATH="/app/config.yaml" \
    LOG_LEVEL="INFO" \
    LOG_FORMAT="text" \
    PYTHONUNBUFFERED=1

# Expose port if running HTTP server
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# Run the MCP server
CMD ["python", "-m", "zerion_mcp_server"]
