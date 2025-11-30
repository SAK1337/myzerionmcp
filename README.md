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

### Wallet & Portfolio
- **getWalletPortfolio**: Returns the portfolio overview of a web3 wallet.
- **listWalletPositions**: Returns a list of wallet positions (supports `filter[positions]=only_complex` for DeFi).
- **getWalletChart**: Returns a portfolio balance chart for a wallet.
- **getWalletPNL**: Returns the Profit and Loss (PnL) details of a web3 wallet.
- **listWalletTransactions**: Returns a list of transactions associated with the wallet (supports advanced filters).

### NFTs
- **getWalletNftPortfolio**: Returns the NFT portfolio overview of a web3 wallet.
- **listWalletNFTCollections**: Returns a list of the NFT collections held by a specific wallet.
- **listWalletNFTPositions**: Returns a list of the NFT positions held by a specific wallet.
- **getNFTById**: Returns a single NFT by its unique identifier.
- **listNFTs**: Returns a list of NFTs by using different parameters.

### Webhooks & Real-Time Notifications (NEW!)
- **createTxSubscription**: Create webhook subscription for real-time transaction notifications.
- **listTxSubscriptions**: List all active transaction subscriptions.
- **getTxSubscription**: Get subscription details by ID.
- **updateTxSubscription**: Update subscription addresses, callback URL, or chain filters.
- **deleteTxSubscription**: Delete a transaction subscription.

### Market Data
- **getFungibleById**: Returns a fungible asset by its unique identifier.
- **getFungibleChart**: Returns the chart for a fungible asset for a selected period.
- **listFungibles**: Returns a paginated list of fungible assets supported by Zerion.
- **listGasPrices**: Provides real-time information on the current gas prices across all supported blockchain networks.
- **listChains**: Returns a list of all chains supported by Zerion.
- **getChainById**: Returns a chain by its unique chain identifier.

### Swaps & Bridges
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

## Webhooks - Real-Time Transaction Notifications

The Zerion MCP Server now supports **transaction subscription webhooks** for real-time wallet activity monitoring. This is critical for production applications because webhooks eliminate inefficient polling, conserve API quotas, and enable sub-second notification latency.

### Why Use Webhooks?

- **Rate Limit Conservation**: Polling wastes API quota (~5K requests/day on free tier). Webhooks push updates only when transactions occur.
- **Real-Time**: Sub-second notifications when monitored wallets transact
- **Scalability**: Monitor hundreds of wallets without quota waste
- **Cost Efficiency**: On paid tiers ($149/mo Builder), webhooks eliminate redundant polling requests

### Architecture Overview

```
┌──────────────┐
│  AI Client   │ (Claude Desktop)
└──────┬───────┘
       │ stdio (MCP protocol)
       ▼
┌──────────────┐
│  MCP Server  │ - Manages subscriptions via API calls
└──────┬───────┘
       │ HTTPS
       ▼
┌──────────────┐
│  Zerion API  │
└──────┬───────┘
       │ Webhooks (HTTP POST)
       ▼
┌──────────────┐
│ Your HTTP    │ - Receives webhook payloads (separate service)
│ Receiver     │
└──────────────┘
```

**Important**: The MCP server manages webhook subscriptions but does NOT receive webhook payloads. You must deploy a separate HTTP service to receive webhook POST requests from Zerion.

### Available Tools

- **`createTxSubscription`** - Create new webhook subscription
- **`listTxSubscriptions`** - List all active subscriptions
- **`getTxSubscription`** - Get subscription details by ID
- **`updateTxSubscription`** - Update addresses, callback URL, or chain filters
- **`deleteTxSubscription`** - Delete subscription

### Example: Create Subscription for Ethereum Address

```
Use the createTxSubscription tool with:
- addresses: ["0x42b9dF65B219B3dD36FF330A4dD8f327A6Ada990"]
- callback_url: "https://webhook.site/your-unique-url"
- chain_ids: ["ethereum", "base"]
```

This creates a subscription that sends webhook notifications to your callback URL whenever the specified address has transactions on Ethereum or Base.

### Example: Create Subscription for Solana Address

```
Use the createTxSubscription tool with:
- addresses: ["8BH9pjtgyZDC4iAQH5ZiYDZ1MDWC98xki2V8NzqqKW3K"]
- callback_url: "https://your-server.com/webhooks/zerion"
- chain_ids: ["solana"]
```

### Webhook Payload Structure

When a monitored address has a new transaction, Zerion sends a POST request to your callback URL with this structure:

```json
{
  "data": {
    "type": "callback",
    "id": "bf300927-3f57-4d00-a01a-f7b75bd9b8de",
    "attributes": {
      "address": "0x42b9dF65B219B3dD36FF330A4dD8f327A6Ada990",
      "callback_url": "https://webhook.site/test",
      "timestamp": "2025-10-16T10:56:50Z"
    },
    "relationships": {
      "subscription": {
        "id": "61f13641-443e-4068-932b-c28edeaefd85",
        "type": "tx-subscriptions"
      }
    }
  },
  "included": [
    {
      "type": "transactions",
      "id": "13de850a-bfa4-54c7-a7bb-fd6371d98894",
      "attributes": {
        "operation_type": "trade",
        "hash": "0x...",
        "mined_at": "2025-10-16T10:56:48Z",
        "status": "confirmed",
        "fee": { ... },
        "transfers": [ ... ]
      },
      "relationships": {
        "chain": { "id": "ethereum", "type": "chains" },
        "dapp": { "id": "uniswap", "type": "dapps" }
      }
    }
  ]
}
```

The `included` array contains full transaction details using the same schema as the `listWalletTransactions` endpoint.

### Setting Up a Webhook Receiver

#### Option 1: Testing with webhook.site (Recommended for Development)

1. Visit https://webhook.site
2. Copy your unique URL (e.g., `https://webhook.site/abc-123-def`)
3. Use that URL as `callback_url` when creating subscriptions
4. View incoming webhooks in real-time on the webhook.site page

#### Option 2: Python Flask Receiver (Production)

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhooks/zerion', methods=['POST'])
def handle_zerion_webhook():
    payload = request.json

    # Extract transaction data
    callback_data = payload['data']
    transactions = payload.get('included', [])

    for tx in transactions:
        if tx['type'] == 'transactions':
            print(f"New transaction: {tx['attributes']['hash']}")
            print(f"Operation: {tx['attributes']['operation_type']}")
            print(f"Chain: {tx['relationships']['chain']['id']}")

    return jsonify({"status": "received"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
```

Deploy this to a public server (Heroku, Vercel, AWS Lambda, etc.) and use the public HTTPS URL as your callback.

#### Option 3: Node.js Express Receiver

```javascript
const express = require('express');
const app = express();

app.use(express.json());

app.post('/webhooks/zerion', (req, res) => {
  const { data, included } = req.body;

  const transactions = included.filter(item => item.type === 'transactions');

  transactions.forEach(tx => {
    console.log(`New ${tx.attributes.operation_type}: ${tx.attributes.hash}`);
  });

  res.status(200).json({ status: 'received' });
});

app.listen(8080, () => console.log('Webhook receiver running on port 8080'));
```

### Webhook Best Practices

1. **Respond Quickly**: Zerion expects < 5 second response time. Do heavy processing asynchronously.
2. **Idempotency**: Webhooks may be delivered multiple times. Check for duplicate transaction IDs.
3. **Retry Policy**: Zerion retries delivery up to 3 times on failure.
4. **HTTPS Required**: Callback URLs must use HTTPS (not HTTP).
5. **No Guaranteed Order**: Don't assume webhook delivery order matches blockchain order.

### Security Considerations

- **Signature Verification**: Future enhancement - webhook payload signing (check Zerion docs)
- **IP Whitelisting**: Consider restricting webhook receiver to Zerion's IP ranges
- **HTTPS Only**: Never use HTTP callback URLs in production

### Troubleshooting Webhooks

#### Webhooks Not Arriving

1. **Check callback URL is publicly accessible**: Test with `curl -X POST https://your-url.com`
2. **Verify subscription is active**: Use `listTxSubscriptions` to confirm subscription exists
3. **Check Zerion dashboard**: Verify API key has webhook permissions
4. **Test with webhook.site first**: Confirm Zerion can reach your infrastructure

#### Rate Limits on Subscription Management

- Developer keys: Limited subscriptions (1-5)
- Contact api@zerion.io for enterprise webhook quotas

---

## Advanced Filtering - Query Optimization

The Zerion API supports powerful filter parameters that are already available in the MCP server but often underutilized. Using filters **reduces API quota usage**, **improves response times**, and enables **precise data queries**.

### Filter Applicability Matrix

| Filter | Endpoints | Use Case |
|--------|-----------|----------|
| **`filter[positions]`** | `getWalletPortfolio`, `listWalletPositions` | Isolate DeFi positions from simple balances |
| **`filter[chain_ids]`** | `listWalletPositions`, `listWalletTransactions`, `getWalletChart`, `listWalletNFTPositions` | Query specific blockchains only |
| **`filter[trash]`** | `listWalletPositions`, `listWalletTransactions`, `listWalletNFTPositions` | Hide spam/dust |
| **`filter[operation_types]`** | `listWalletTransactions` | Filter by transaction type (trade, transfer, execute) |
| **`filter[position_types]`** | `listWalletPositions` | Filter by DeFi category (staked, deposit, loan, reward) |
| **`filter[fungible_ids]`** | `listWalletPositions`, `listWalletTransactions` | Track specific tokens only |

### DeFi Position Filtering (`only_complex`)

**Problem**: By default, `listWalletPositions` returns simple token balances. DeFi protocols (staking, LPs, lending) are excluded.

**Solution**: Use `filter[positions]=only_complex` to get **only DeFi positions**.

#### Example: Get DeFi Positions Only

```
Use listWalletPositions with:
- address: "0x42b9dF65B219B3dD36FF330A4dD8f327A6Ada990"
- filter[positions]: "only_complex"
- filter[trash]: "only_non_trash"
- currency: "usd"
```

**Result**: Returns staking positions (e.g., staked ETH), liquidity pool tokens (Uniswap, Curve), lending positions (Aave, Compound), and yield farming positions. Excludes simple ERC-20 balances.

**Use Cases**:
- DeFi analytics dashboards
- Institutional risk management (track complex positions separately)
- Yield farming trackers
- Portfolio categorization for tax reporting

#### Filter Options

- **`only_simple`** (default): Only wallet-type positions (basic token balances)
- **`only_complex`**: Only DeFi protocol positions (staking, LP, lending)
- **`no_filter`**: Both simple and complex positions

### Chain Filtering (`filter[chain_ids]`)

**Problem**: Fetching positions across all 50+ chains wastes quota and returns irrelevant data.

**Solution**: Use `filter[chain_ids]` to query specific blockchains.

#### Example: Ethereum + Base Only

```
Use listWalletTransactions with:
- address: "0x..."
- filter[chain_ids]: "ethereum,base"
- filter[trash]: "only_non_trash"
```

**Result**: Only transactions on Ethereum and Base. Ignores activity on Polygon, Arbitrum, Optimism, etc.

#### Example: Single Chain (Optimism)

```
Use listWalletPositions with:
- address: "0x..."
- filter[chain_ids]: "optimism"
```

**Use Cases**:
- L2-focused analytics (Base, Optimism, Arbitrum)
- Cross-chain comparison (Ethereum vs. L2s)
- Mainnet-only queries

**Valid Chain IDs**: `ethereum`, `base`, `optimism`, `arbitrum`, `polygon`, `solana`, `binance-smart-chain`, `avalanche`, `fantom`, `gnosis`, etc. Use `listChains` to see all supported chains.

### Spam Filtering (`filter[trash]`)

**Problem**: Wallet transaction history polluted with spam tokens, dust, and airdrop scams.

**Solution**: Use `filter[trash]=only_non_trash` to hide spam.

#### Example: Clean Transaction History

```
Use listWalletTransactions with:
- address: "0x..."
- filter[trash]: "only_non_trash"
- page[size]: 100
```

**Result**: Clean transaction history without spam tokens or dust transfers.

#### Filter Options

- **`only_non_trash`**: Hide spam/dust (recommended for user-facing apps)
- **`only_trash`**: Show only spam/dust (for security monitoring)
- **`no_filter`** (default): Show all transactions

**Use Cases**:
- User-facing wallets (clean UI)
- Portfolio analytics (exclude noise)
- Tax reporting (ignore spam airdrops)

### Transaction Type Filtering (`filter[operation_types]`)

**Problem**: Need to analyze specific transaction types (e.g., only swaps, only transfers).

**Solution**: Use `filter[operation_types]` to isolate transaction categories.

#### Example: Trades Only

```
Use listWalletTransactions with:
- address: "0x..."
- filter[operation_types]: "trade"
- filter[chain_ids]: "ethereum,base"
```

**Result**: Only DEX swaps and trades. Excludes transfers, approvals, contract executions.

#### Available Operation Types

- **`trade`**: Token swaps (Uniswap, 1inch, etc.)
- **`transfer`**: Simple token transfers
- **`execute`**: Smart contract interactions
- **`approve`**: Token approvals
- **`deposit`**: Protocol deposits
- **`withdraw`**: Protocol withdrawals

**Use Cases**:
- Trading analytics (volume, frequency)
- Transfer tracking (payroll, payments)
- Smart contract interaction audits

### Position Type Filtering (`filter[position_types]`)

**Problem**: DeFi positions span many categories (staking, lending, rewards). Need to isolate specific types.

**Solution**: Use `filter[position_types]` for granular DeFi categorization.

#### Example: Staking + Rewards Only

```
Use listWalletPositions with:
- address: "0x..."
- filter[positions]: "only_complex"
- filter[position_types]: "staked,reward"
```

**Result**: Only staked assets and claimable rewards. Excludes LP positions, loans, deposits.

#### Available Position Types

- **`wallet`**: Simple balance
- **`deposit`**: Lending protocol deposits (Aave, Compound)
- **`loan`**: Borrowed assets
- **`staked`**: Staked tokens (ETH staking, governance staking)
- **`reward`**: Claimable rewards
- **`locked`**: Vested/locked tokens
- **`margin`**: Margin trading positions
- **`airdrop`**: Airdrop eligibility

**Use Cases**:
- Staking dashboards
- Yield optimization
- Loan/collateralization tracking
- Rewards harvesting

### Query Optimization Best Practices

#### 1. Use Filters to Reduce Quota Usage

**Bad** (fetches all data, filters client-side):
```
- Get all positions for address
- Filter out spam in your app
- Filter to Ethereum-only in your app
```
**Cost**: ~1000 positions returned, large response

**Good** (filter at API level):
```
Use listWalletPositions with:
- filter[chain_ids]: "ethereum"
- filter[trash]: "only_non_trash"
```
**Cost**: ~50 positions returned, 20x smaller response

#### 2. Combine Filters for Precision

**Example: DeFi-Only, Ethereum, No Spam**
```
Use listWalletPositions with:
- filter[positions]: "only_complex"
- filter[chain_ids]: "ethereum"
- filter[trash]: "only_non_trash"
- currency: "usd"
- sort: "value"
```

**Result**: High-value Ethereum DeFi positions only. Perfect for risk dashboards.

#### 3. Page Size Control

```
Use listWalletTransactions with:
- page[size]: 50
- filter[trash]: "only_non_trash"
```

Smaller pages = faster responses, less quota per request.

### Common Filter Combinations

| Use Case | Filters |
|----------|---------|
| **Clean transaction feed** | `filter[trash]=only_non_trash`, `filter[operation_types]=trade,transfer` |
| **DeFi risk dashboard** | `filter[positions]=only_complex`, `filter[chain_ids]=ethereum`, `sort=value` |
| **L2 trading analytics** | `filter[chain_ids]=base,optimism,arbitrum`, `filter[operation_types]=trade` |
| **Staking tracker** | `filter[positions]=only_complex`, `filter[position_types]=staked,reward` |
| **NFT portfolio (no spam)** | `filter[trash]=only_non_trash` on `listWalletNFTPositions` |

---

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
