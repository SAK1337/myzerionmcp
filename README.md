# Zerion MCP Server

A production-ready [Model Context Protocol](https://modelcontextprotocol.io) (MCP) server that provides AI assistants with access to the Zerion API for cryptocurrency portfolio management, DeFi positions, NFTs, and market data.

## Features

- 🔌 **Auto-generated Tools**: Automatically exposes Zerion API endpoints as MCP tools via OpenAPI specification
- ⚙️ **Flexible Configuration**: YAML config files with environment variable overrides
- 📝 **Structured Logging**: JSON and text formats with sensitive data redaction
- 🛡️ **Robust Error Handling**: Custom exceptions with detailed context and troubleshooting hints
- ✅ **Comprehensive Tests**: Unit and integration tests with pytest
- 🚀 **Async HTTP**: Non-blocking API calls with httpx

## Available Functions

- **getChainById**: Returns a chain by its unique chain identifier.
- **getFungibleById**: Returns a fungible asset by its unique identifier.
- **getFungibleChart**: Returns the chart for a fungible asset for a selected period.
- **getNFTById**: Returns a single NFT by its unique identifier.
- **getWalletChart**: Returns a portfolio balance chart for a wallet.
- **getWalletNftPortfolio**: Returns the NFT portfolio overview of a web3 wallet.
- **getWalletPNL**: Returns the Profit and Loss (PnL) details of a web3 wallet.
- **getWalletPortfolio**: Returns the portfolio overview of a web3 wallet.
- **listChains**: Returns a list of all chains supported by Zerion.
- **listFungibles**: Returns a paginated list of fungible assets supported by Zerion.
- **listGasPrices**: Provides real-time information on the current gas prices across all supported blockchain networks.
- **listNFTs**: Returns a list of NFTs by using different parameters.
- **listWalletNFTCollections**: Returns a list of the NFT collections held by a specific wallet.
- **listWalletNFTPositions**: Returns a list of the NFT positions held by a specific wallet.
- **listWalletPositions**: Returns a list of wallet positions.
- **listWalletTransactions**: Returns a list of transactions associated with the wallet.
- **swapFungibles**: Provides a list of fungibles available for bridge exchange.
- **swapOffers**: Provides a comprehensive overview of relevant trades and bridge exchanges.

## Requirements

### For Docker (Recommended)
- Docker 20.10 or higher
- Docker Compose V2
- Zerion API key ([Get one here](https://developers.zerion.io/))

### For Native Python Installation
- Python 3.11 or higher
- Zerion API key ([Get one here](https://developers.zerion.io/))

## Installation

### Using Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/SAK1337/myzerionmcp.git
cd myzerionmcp

# Create .env file with your API key
cp .env.example .env
# Edit .env and set ZERION_API_KEY

# Start with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f
```

See [DOCKER.md](DOCKER.md) for detailed Docker deployment guide.

### From Source

```bash
# Clone the repository
git clone https://github.com/SAK1337/myzerionmcp.git
cd myzerionmcp

# Install the package
pip install -e .

# For development (includes testing dependencies)
pip install -e ".[dev]"
```

### From PyPI (when published)

```bash
pip install zerion-mcp-server
```

## Quick Start

### 1. Set up your API key

```bash
export ZERION_API_KEY="Bearer your-api-key-here"
```

### 2. Run the server

```bash
zerion-mcp-server
```

### 3. Connect with an MCP client

The server will start and listen for MCP protocol connections. You can connect it to AI assistants like Claude Desktop.

#### Claude Desktop Configuration

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "zerion": {
      "command": "zerion-mcp-server",
      "env": {
        "ZERION_API_KEY": "Bearer your-api-key-here"
      }
    }
  }
}
```

## Configuration

### Configuration File

Create a `config.yaml` file in your working directory:

```yaml
# Server configuration
name: "Zerion API"
base_url: "https://api.zerion.io"
oas_url: "https://raw.githubusercontent.com/smart-mcp-proxy/zerion-mcp-server/main/zerion_mcp_server/openapi_zerion.yaml"

# API authentication
api_key: "${ZERION_API_KEY}"  # Environment variable substitution

# Logging configuration
logging:
  level: "INFO"      # DEBUG, INFO, WARN, ERROR
  format: "text"     # text or json
```

See [`config.example.yaml`](config.example.yaml) for a complete example.

### Environment Variables

Environment variables override config file values:

| Variable | Description | Default |
|----------|-------------|---------|
| `ZERION_API_KEY` | Zerion API key (required) | - |
| `ZERION_BASE_URL` | Zerion API base URL | `https://api.zerion.io` |
| `ZERION_OAS_URL` | OpenAPI spec URL | GitHub raw URL |
| `CONFIG_PATH` | Path to config.yaml | `./config.yaml` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `LOG_FORMAT` | Logging format (text/json) | `text` |

## Usage Examples

Once connected to an MCP client (like Claude), you can query Zerion data:

### Portfolio Balance

```
Get the portfolio balance for wallet 0x1234...
```

The server exposes tools like `getWalletChart`, `getWalletPositions`, etc.

### DeFi Positions

```
Show me the DeFi positions for address 0xabcd...
```

### NFT Collections

```
List NFTs owned by 0x5678...
```

All Zerion API endpoints are automatically available as MCP tools. See the [Zerion API documentation](https://developers.zerion.io/reference) for available operations.

## Development

### Setup Development Environment

```bash
# Clone and install with dev dependencies
git clone https://github.com/SAK1337/myzerionmcp.git
cd myzerionmcp
pip install -e ".[dev]"

# Set up API key
export ZERION_API_KEY="Bearer your-test-key"
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=zerion_mcp_server --cov-report=html

# Run specific test file
pytest tests/test_config.py

# Run with verbose output
pytest -v
```

### Code Quality

```bash
# Type checking (if mypy is installed)
mypy zerion_mcp_server

# Linting (if ruff is installed)
ruff check zerion_mcp_server
```

## Troubleshooting

### Common Issues

#### "Configuration error: Missing required configuration: api_key"

**Solution**: Set the `ZERION_API_KEY` environment variable:

```bash
export ZERION_API_KEY="Bearer your-api-key-here"
```

#### "Timeout loading OpenAPI specification"

**Solution**: Check your internet connection. The server needs to download the OpenAPI spec from GitHub.

#### "Unauthorized: Invalid or missing API key"

**Solution**: Verify your API key is correct and includes the "Bearer " prefix:

```bash
export ZERION_API_KEY="Bearer your-actual-key"
```

#### "Rate limit exceeded"

**Solution**: Wait for the rate limit window to reset. Check the error message for `retry_after_sec` value.

### Debug Mode

Enable debug logging for detailed information:

```bash
export LOG_LEVEL="DEBUG"
zerion-mcp-server
```

Or in `config.yaml`:

```yaml
logging:
  level: "DEBUG"
  format: "json"  # Structured logs for analysis
```

### Log Interpretation

- **INFO**: Normal operation (startup, requests)
- **WARN**: Potential issues (slow operations)
- **ERROR**: Failures (API errors, network issues)
- **DEBUG**: Detailed traces (request/response bodies)

## Architecture

```
┌─────────────────┐
│   MCP Client    │ (e.g., Claude Desktop)
│  (AI Assistant) │
└────────┬────────┘
         │ MCP Protocol
         │
┌────────▼────────┐
│  FastMCP Server │
│                 │
│  ┌───────────┐  │
│  │ Config    │  │ (YAML + Env)
│  │ Manager   │  │
│  └───────────┘  │
│                 │
│  ┌───────────┐  │
│  │  Logger   │  │ (Structured)
│  └───────────┘  │
│                 │
│  ┌───────────┐  │
│  │  Error    │  │ (Custom Exceptions)
│  │  Handler  │  │
│  └───────────┘  │
│                 │
│  ┌───────────┐  │
│  │ HTTP      │  │ (httpx AsyncClient)
│  │ Client    │  │
│  └─────┬─────┘  │
└────────┼────────┘
         │
         │ HTTPS
         │
┌────────▼────────┐
│   Zerion API    │
│                 │
│  - Portfolios   │
│  - DeFi         │
│  - NFTs         │
│  - Transactions │
└─────────────────┘
```

## Tech Stack

- **Python 3.11+**: Core language
- **FastMCP**: MCP server framework with OpenAPI integration
- **httpx**: Async HTTP client
- **PyYAML**: Configuration parsing
- **pytest**: Testing framework

## Contributing

Contributions are welcome! Please follow these guidelines:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature`
3. **Write tests** for your changes
4. **Ensure tests pass**: `pytest`
5. **Submit a pull request**

### Development Workflow

- Follow PEP 8 style guidelines
- Add type hints to function signatures
- Write docstrings for modules and functions
- Update tests for any code changes
- Keep commits focused and atomic

## License

MIT License - see [LICENSE](LICENSE) file for details

## Support

- **Issues**: [GitHub Issues](https://github.com/SAK1337/myzerionmcp/issues)
- **Zerion API Docs**: [developers.zerion.io](https://developers.zerion.io/)
- **MCP Specification**: [modelcontextprotocol.io](https://modelcontextprotocol.io/)

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and changes
