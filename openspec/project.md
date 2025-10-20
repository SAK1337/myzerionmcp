# Project Context

## Purpose
MCP (Model Context Protocol) server that provides AI assistants with access to the Zerion API. This server enables AI models to query cryptocurrency portfolios, DeFi positions, NFTs, and market data through a standardized protocol interface.

## Tech Stack
- **Python 3.11+**: Core language
- **FastMCP**: MCP server framework with OpenAPI integration
- **httpx**: Async HTTP client for API requests
- **PyYAML**: OpenAPI specification parsing
- **OpenAPI**: API definition standard (Zerion's spec hosted on GitHub)
- **Hatchling**: Build system

## Project Conventions

### Code Style
- Follow PEP 8 Python style guidelines
- Use snake_case for functions and variables
- Type hints preferred for function signatures
- Docstrings for modules and main functions
- Keep imports organized: standard library, third-party, local

### Architecture Patterns
- **OpenAPI-driven design**: Server auto-generates tools from Zerion's OpenAPI spec
- **Environment-based configuration**: API keys via environment variables
- **Async HTTP**: Uses httpx.AsyncClient for non-blocking API calls
- **Single responsibility**: Server focuses solely on proxying Zerion API through MCP
- **Remote spec loading**: Fetches OpenAPI spec from GitHub at runtime

### Testing Strategy
- Manual testing through MCP client interactions
- Environment validation (ZERION_API_KEY checks)
- Future: Add unit tests for configuration and error handling

### Git Workflow
- Standard .gitignore for Python projects (excludes __pycache__, venv, .env, etc.)
- Keep sensitive data (API keys) in environment variables
- Track OpenAPI spec locally for reference but load from remote URL

## Domain Context
- **Zerion**: Web3 portfolio management platform aggregating DeFi, NFTs, and cryptocurrency data
- **MCP**: Model Context Protocol - enables AI assistants to interact with external tools and data sources
- **API Authorization**: Uses Bearer token authentication via Authorization header
- **Base URL**: https://api.zerion.io

## Important Constraints
- **Required Environment Variable**: `ZERION_API_KEY` must be set with format "Bearer your-api-key-here"
- **Python Version**: Minimum Python 3.11 required
- **Network Dependency**: Requires internet access to fetch OpenAPI spec and call Zerion API
- **API Rate Limits**: Subject to Zerion API rate limiting (check their documentation)

## External Dependencies
- **Zerion API**: https://api.zerion.io - primary data source
- **OpenAPI Spec**: Hosted on GitHub (smart-mcp-proxy/zerion-mcp-server repository)
- **FastMCP Framework**: Handles MCP protocol implementation and OpenAPI conversion
