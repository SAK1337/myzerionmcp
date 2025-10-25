# Docker Deployment Guide

This guide explains how to run the Zerion MCP Server using Docker.

## Quick Start

### 1. Build the Docker Image

```bash
docker build -t zerion-mcp-server .
```

### 2. Run with Docker Compose (Recommended)

```bash
# Create .env file from example
cp .env.example .env

# Edit .env and add your API key
# ZERION_API_KEY=zk_dev_your_actual_key

# Start the service
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the service
docker-compose down
```

### 3. Run with Docker CLI

```bash
docker run -d \
  --name zerion-mcp-server \
  -e ZERION_API_KEY="zk_dev_your_api_key_here" \
  -e LOG_LEVEL="INFO" \
  -v $(pwd)/config.yaml:/app/config.yaml:ro \
  -v $(pwd)/logs:/app/logs \
  -p 8000:8000 \
  zerion-mcp-server
```

## Configuration

### Environment Variables

Set these in your `.env` file or pass them with `-e`:

| Variable | Description | Default |
|----------|-------------|---------|
| `ZERION_API_KEY` | Your Zerion API key (required) | - |
| `CONFIG_PATH` | Path to config file | `/app/config.yaml` |
| `LOG_LEVEL` | Logging level (DEBUG/INFO/WARN/ERROR) | `INFO` |
| `LOG_FORMAT` | Log format (text/json) | `text` |

### Volume Mounts

- **Config**: `-v ./config.yaml:/app/config.yaml:ro` (read-only)
- **Logs**: `-v ./logs:/app/logs` (persistent logs)

## Production Deployment

### Using Docker Compose in Production

```yaml
version: '3.8'

services:
  zerion-mcp-server:
    image: zerion-mcp-server:latest
    container_name: zerion-mcp-server-prod
    environment:
      - ZERION_API_KEY=${ZERION_API_KEY}
      - LOG_LEVEL=INFO
      - LOG_FORMAT=json
    volumes:
      - ./config.production.yaml:/app/config.yaml:ro
      - /var/log/zerion-mcp:/app/logs
    restart: always
    healthcheck:
      test: ["CMD", "python", "-c", "import sys; sys.exit(0)"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### Build for Production

```bash
# Build optimized image
docker build --no-cache -t zerion-mcp-server:latest .

# Tag for registry
docker tag zerion-mcp-server:latest your-registry/zerion-mcp-server:latest

# Push to registry
docker push your-registry/zerion-mcp-server:latest
```

## Troubleshooting

### View Logs

```bash
# Docker Compose
docker-compose logs -f zerion-mcp-server

# Docker CLI
docker logs -f zerion-mcp-server
```

### Access Container Shell

```bash
# Docker Compose
docker-compose exec zerion-mcp-server /bin/bash

# Docker CLI
docker exec -it zerion-mcp-server /bin/bash
```

### Check Container Status

```bash
# Docker Compose
docker-compose ps

# Docker CLI
docker ps -a | grep zerion
```

### Rebuild After Code Changes

```bash
# Docker Compose
docker-compose up -d --build

# Docker CLI
docker build --no-cache -t zerion-mcp-server .
docker stop zerion-mcp-server
docker rm zerion-mcp-server
docker run ... # (use same run command as before)
```

## MCP Client Configuration

### For Claude Desktop (with Docker)

If you're running the server in Docker on the same machine:

```json
{
  "mcpServers": {
    "zerion": {
      "command": "docker",
      "args": [
        "exec",
        "-i",
        "zerion-mcp-server",
        "python",
        "-m",
        "zerion_mcp_server"
      ]
    }
  }
}
```

### For Remote Docker Host

If running on a remote server, expose via stdio-over-network or use HTTP transport.

## Multi-Architecture Builds

To build for multiple platforms (e.g., ARM64 for Apple Silicon):

```bash
# Create buildx builder
docker buildx create --name multiarch --use

# Build for multiple platforms
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t your-registry/zerion-mcp-server:latest \
  --push \
  .
```

## Security Best Practices

1. **Never commit `.env` files** - Add to `.gitignore`
2. **Use secrets management** for production API keys
3. **Run as non-root user** (add to Dockerfile):
   ```dockerfile
   RUN useradd -m -u 1000 appuser
   USER appuser
   ```
4. **Keep base image updated** - Regularly rebuild with latest Python image
5. **Scan for vulnerabilities**:
   ```bash
   docker scan zerion-mcp-server
   ```

## Resource Limits

Add resource constraints in `docker-compose.yml`:

```yaml
services:
  zerion-mcp-server:
    # ... other config ...
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
```

## Support

For Docker-specific issues, check:
- Container logs: `docker logs zerion-mcp-server`
- Container stats: `docker stats zerion-mcp-server`
- Docker inspect: `docker inspect zerion-mcp-server`
