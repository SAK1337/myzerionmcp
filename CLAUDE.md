# Zerion MCP Server - AI Assistant Guide

## Project Overview

**Zerion MCP Server** is a production-ready Model Context Protocol (MCP) server that provides AI assistants with access to the Zerion API for cryptocurrency portfolio management, DeFi positions, NFTs, and blockchain market data.

### Purpose
Enable AI assistants like Claude to query Web3 data through the MCP protocol by:
- Auto-generating tools from Zerion's OpenAPI specification
- Providing structured access to 100+ blockchain networks
- Supporting DeFi protocols, NFT metadata, and transaction history
- Enabling real-time webhook notifications for wallet activity

### Key Capabilities
- **Multi-Chain Aggregation**: Query 100+ blockchains in a single API call (Ethereum, Base, Polygon, Arbitrum, Optimism, Solana, etc.)
- **DeFi Protocol Coverage**: Track 8,000+ DeFi protocols (Uniswap, Aave, Curve, Lido, etc.)
- **NFT Metadata**: Comprehensive NFT data with images, floor prices, and collection details
- **Webhooks**: Real-time transaction notifications (eliminates polling)
- **Advanced Filtering**: Chain-specific, DeFi-only, spam filtering, transaction type filtering
- **Automatic Pagination**: Handle large result sets (5000+ items) with cursor-based pagination
- **Retry Logic**: Exponential backoff for rate limits (429) and wallet indexing (202)
- **Multi-Currency**: USD, ETH, EUR, BTC denomination support
- **Testnet Support**: Test on Sepolia, Monad, Base Sepolia, etc. via X-Env header

## Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Runtime** | Python 3.11+ | Core language |
| **Framework** | FastMCP 2.8.0+ | MCP protocol implementation with OpenAPI integration |
| **HTTP Client** | httpx (async) | Non-blocking API calls |
| **Config** | PyYAML | YAML configuration parsing |
| **Server** | uvicorn/starlette | ASGI server |
| **Retry** | tenacity | Automatic retry with exponential backoff |
| **Testing** | pytest + pytest-asyncio | Unit and integration tests |
| **Build** | hatchling | Python package build system |

## Architecture

```
┌─────────────────┐
│   MCP Client    │ (Claude Desktop, AI assistants)
│  (AI Assistant) │
└────────┬────────┘
         │ stdio (MCP protocol)
         │
┌────────▼────────┐
│  FastMCP Server │
│                 │
│  ┌───────────┐  │
│  │ Config    │  │ (config.yaml + env vars)
│  │ Manager   │  │
│  └───────────┘  │
│                 │
│  ┌───────────┐  │
│  │  Logger   │  │ (JSON/text, redaction)
│  └───────────┘  │
│                 │
│  ┌───────────┐  │
│  │  Error    │  │ (Custom exceptions)
│  │  Handler  │  │
│  └───────────┘  │
│                 │
│  ┌───────────┐  │
│  │ Retry     │  │ (httpx + tenacity)
│  │ Client    │  │
│  └─────┬─────┘  │
└────────┼────────┘
         │ HTTPS
         │
┌────────▼────────┐
│   Zerion API    │ (api.zerion.io)
│                 │
│  - Portfolios   │
│  - DeFi         │
│  - NFTs         │
│  - Webhooks     │
└─────────────────┘
```

## Project Structure

```
myzerionmcp/
├── zerion_mcp_server/        # Main package
│   ├── __init__.py           # Entry point, main()
│   ├── __main__.py           # CLI entry
│   ├── config.py             # Configuration management
│   ├── logger.py             # Structured logging
│   ├── errors.py             # Custom exceptions
│   ├── retry_client.py       # HTTP client with retry logic
│   ├── pagination.py         # Pagination helpers
│   └── openapi_zerion.yaml   # Zerion API spec (reference)
├── tests/                    # pytest test suite
├── openspec/                 # OpenSpec change management
│   ├── AGENTS.md            # OpenSpec workflow guide
│   ├── project.md           # Project context
│   ├── specs/               # Specification documents
│   └── changes/             # Change proposals
├── .claude/                  # Claude Code configuration
│   ├── commands/            # Custom slash commands
│   └── settings.local.json  # Local settings
├── config.yaml              # Server configuration
├── .env                     # Environment variables (API keys)
├── pyproject.toml           # Python package metadata
├── README.md                # User documentation
└── CLAUDE.md                # This file (AI assistant guide)
```

## Code Conventions

### Style Guidelines
- **PEP 8 compliance**: Follow Python style guidelines
- **snake_case**: For functions, variables, file names
- **Type hints**: Preferred for function signatures
- **Docstrings**: Required for modules and main functions
- **Import order**: Standard library → third-party → local modules

### Architecture Patterns
- **OpenAPI-driven design**: Tools auto-generated from Zerion's OpenAPI spec
- **Environment-based config**: Sensitive data in .env (never committed)
- **Async HTTP**: Uses httpx.AsyncClient for non-blocking calls
- **Single responsibility**: Each module has one clear purpose
- **Remote spec loading**: Fetches OpenAPI spec from GitHub at runtime
- **Dependency injection**: Config and logger passed to components

### Error Handling
- **Custom exceptions**: Located in `errors.py`
  - `ZerionAPIError`: Base exception for all API errors
  - `RateLimitError`: 429 responses (rate limiting)
  - `WalletIndexingError`: 202 responses (wallet being indexed)
  - `ConfigurationError`: Missing/invalid configuration
- **Actionable messages**: Include troubleshooting hints and next steps
- **Automatic retry**: Transparent retry for 429 and 202 responses

### Testing Strategy
- **Unit tests**: Test individual components (config, logger, errors)
- **Integration tests**: Test API calls with mocked responses (respx)
- **Async tests**: pytest-asyncio for async function testing
- **Coverage**: Aim for >80% code coverage
- **Run tests**: `pytest` or `pytest --cov=zerion_mcp_server`

## Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `ZERION_API_KEY` | Zerion API key (format: "Bearer your-key") | Yes | - |
| `ZERION_BASE_URL` | Zerion API base URL | No | https://api.zerion.io |
| `ZERION_OAS_URL` | OpenAPI spec URL | No | GitHub raw URL |
| `CONFIG_PATH` | Path to config.yaml | No | ./config.yaml |
| `LOG_LEVEL` | Logging level (DEBUG/INFO/WARN/ERROR) | No | INFO |
| `LOG_FORMAT` | Log format (text/json) | No | text |

**Get an API key**: https://developers.zerion.io/

## Configuration

Configuration sources (priority order):
1. **Environment variables** (highest priority)
2. **config.yaml** file
3. **Defaults** in code

### Example config.yaml

```yaml
# Server configuration
name: "Zerion API"
base_url: "https://api.zerion.io"
oas_url: "https://raw.githubusercontent.com/smart-mcp-proxy/zerion-mcp-server/main/zerion_mcp_server/openapi_zerion.yaml"

# API authentication
api_key: "${ZERION_API_KEY}"  # Environment variable substitution

# Logging
logging:
  level: "INFO"
  format: "text"

# Retry policy
retry_policy:
  max_attempts: 5
  base_delay: 1
  max_delay: 60
  exponential_base: 2

# Wallet indexing (202 responses)
wallet_indexing:
  retry_delay: 3
  max_retries: 3
  auto_retry: true

# Pagination
pagination:
  default_page_size: 100
  max_auto_pages: 50
```

## Available Tools (MCP)

The server exposes all Zerion API endpoints as MCP tools:

### Wallet & Portfolio
- `getWalletPortfolio`: Portfolio overview (total value, change %)
- `listWalletPositions`: Token balances and DeFi positions
- `getWalletChart`: Historical balance chart
- `getWalletPNL`: Profit and Loss details
- `listWalletTransactions`: Transaction history with filters

### NFTs
- `getWalletNftPortfolio`: NFT portfolio overview
- `listWalletNFTCollections`: NFT collections held
- `listWalletNFTPositions`: Individual NFT positions
- `getNFTById`: Single NFT by ID
- `listNFTs`: List NFTs with filters

### Webhooks
- `createTxSubscription`: Create transaction webhook
- `listTxSubscriptions`: List active subscriptions
- `getTxSubscription`: Get subscription details
- `updateTxSubscription`: Update subscription
- `deleteTxSubscription`: Delete subscription

### Market Data
- `getFungibleById`: Get token by ID
- `getFungibleChart`: Token price chart
- `listFungibles`: List supported tokens
- `listGasPrices`: Real-time gas prices
- `listChains`: List supported chains
- `getChainById`: Get chain details

### Swaps & Bridges
- `swapFungibles`: Get available swap options
- `swapOffers`: Get swap/bridge quotes

## Development Workflow

### Setup
```bash
git clone https://github.com/SAK1337/myzerionmcp.git
cd myzerionmcp
pip install -e ".[dev]"
export ZERION_API_KEY="Bearer your-api-key"
```

### Running
```bash
# Run server
zerion-mcp-server

# With custom config
CONFIG_PATH=/path/to/config.yaml zerion-mcp-server

# Debug mode
LOG_LEVEL=DEBUG zerion-mcp-server
```

### Testing
```bash
# Run all tests
pytest

# With coverage
pytest --cov=zerion_mcp_server --cov-report=html

# Specific test file
pytest tests/test_config.py

# Verbose mode
pytest -v
```

### Making Changes
1. **Read existing code** before modifying
2. **Write tests** for new functionality
3. **Run pytest** to ensure tests pass
4. **Update documentation** (README.md if user-facing)
5. **Follow PEP 8** style guidelines
6. **Add type hints** to new functions
7. **Test manually** with Claude Desktop or MCP inspector

## Domain Context

### Zerion API
- **Base URL**: https://api.zerion.io
- **Auth**: Bearer token in Authorization header
- **Rate Limits**: 2 RPS (free), 50 RPS (Builder $149/mo), 150 RPS (Pro $599/mo)
- **Docs**: https://developers.zerion.io/reference

### Model Context Protocol (MCP)
- **Spec**: https://modelcontextprotocol.io/
- **Purpose**: Standardized protocol for AI assistants to interact with external tools
- **Transport**: stdio (standard input/output)
- **Tools**: Exposed as JSON-RPC methods

### Key Concepts
- **Multi-chain aggregation**: Single API call returns data from 100+ chains
- **DeFi positions**: Complex protocol positions (staking, LP, lending) vs. simple token balances
- **Cursor pagination**: Use `page[after]` for large result sets
- **Spam filtering**: `filter[trash]=only_non_trash` hides spam tokens
- **Chain filtering**: `filter[chain_ids]=ethereum,base` limits to specific chains

## Important Constraints

### Required
- **Python 3.11+**: Minimum version (uses modern async features)
- **ZERION_API_KEY**: Must be set with "Bearer " prefix
- **Internet access**: Fetches OpenAPI spec from GitHub
- **MCP client**: Server requires MCP-compatible client (Claude Desktop, etc.)

### Rate Limits
- **Developer tier**: 2 RPS, ~5,000 requests/day
- **Builder tier**: 50 RPS, ~500,000 requests/day
- **Pro tier**: 150 RPS, ~1.5M requests/day
- **Automatic retry**: Server handles 429 responses with exponential backoff

### Wallet Indexing
- **202 Accepted**: New wallets take 2-10 seconds to index
- **Automatic retry**: Server retries 202 responses 3 times (3s delay)
- **Total wait**: Up to 9 seconds for indexing completion

## Common Patterns

### Query DeFi positions only
```python
# Use filter[positions]=only_complex to exclude simple balances
params = {
    "address": "0x...",
    "filter[positions]": "only_complex",
    "filter[trash]": "only_non_trash",
    "currency": "usd"
}
```

### Filter by specific chains
```python
params = {
    "address": "0x...",
    "filter[chain_ids]": "ethereum,base,optimism",
    "currency": "usd"
}
```

### Get clean transaction history
```python
params = {
    "address": "0x...",
    "filter[trash]": "only_non_trash",
    "filter[operation_types]": "trade,transfer",
    "page[size]": 100
}
```

### Use webhooks instead of polling
```python
# Bad: Polling (wastes quota)
while True:
    txs = get_transactions(address)
    time.sleep(10)  # 8,640 requests/day!

# Good: Webhooks (push notifications)
create_tx_subscription(
    addresses=["0x..."],
    callback_url="https://your-server.com/webhooks"
)  # 1 request total
```

## Troubleshooting

### "Missing required configuration: api_key"
**Solution**: Set `ZERION_API_KEY` environment variable
```bash
export ZERION_API_KEY="Bearer your-api-key-here"
```

### "Rate limit exceeded"
**Solution**: Wait for retry_after duration or upgrade tier
- Check error message for retry_after_sec
- Implement client-side caching
- Use webhooks instead of polling

### "Wallet indexing timeout"
**Solution**: Increase retry settings or wait longer
```yaml
wallet_indexing:
  retry_delay: 5
  max_retries: 5
```

### Tests failing
**Solution**: Check dependencies and API key
```bash
pip install -e ".[dev]"
export ZERION_API_KEY="Bearer test-key"
pytest -v
```

## OpenSpec Change Management

<!-- OPENSPEC:START -->
# OpenSpec Instructions

These instructions are for AI assistants working in this project.

Always open `@/openspec/AGENTS.md` when the request:
- Mentions planning or proposals (words like proposal, spec, change, plan)
- Introduces new capabilities, breaking changes, architecture shifts, or big performance/security work
- Sounds ambiguous and you need the authoritative spec before coding

Use `@/openspec/AGENTS.md` to learn:
- How to create and apply change proposals
- Spec format and conventions
- Project structure and guidelines

Keep this managed block so 'openspec update' can refresh the instructions.

<!-- OPENSPEC:END -->

## Quick Reference

### File Locations
- Entry point: `zerion_mcp_server/__init__.py`
- Configuration: `zerion_mcp_server/config.py`
- HTTP client: `zerion_mcp_server/retry_client.py`
- Pagination: `zerion_mcp_server/pagination.py`
- Errors: `zerion_mcp_server/errors.py`
- Tests: `tests/`

### Useful Commands
```bash
# Run server
zerion-mcp-server

# Test suite
pytest

# Coverage report
pytest --cov=zerion_mcp_server --cov-report=html

# Debug logging
LOG_LEVEL=DEBUG zerion-mcp-server

# Install dev dependencies
pip install -e ".[dev]"
```

### Documentation Files
- User guide: `README.md` (comprehensive feature documentation)
- This file: `CLAUDE.md` (AI assistant guide)
- Docker guide: `DOCKER.md`
- Changelog: `CHANGELOG.md`
- OpenSpec: `openspec/AGENTS.md`