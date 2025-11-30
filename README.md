# Zerion MCP Server

A production-ready [Model Context Protocol](https://modelcontextprotocol.io) (MCP) server that provides AI assistants with access to the Zerion API for cryptocurrency portfolio management, DeFi positions, NFTs, and market data.

## Features

- 🔌 **Auto-generated Tools**: Automatically exposes Zerion API endpoints as MCP tools via OpenAPI specification
- ⚙️ **Flexible Configuration**: YAML config files with environment variable overrides
- 📝 **Structured Logging**: JSON and text formats with sensitive data redaction
- 🛡️ **Robust Error Handling**: Custom exceptions with detailed context and troubleshooting hints
- 🔁 **Automatic Retry Logic**: Exponential backoff for rate limits (429) and wallet indexing (202)
- 📄 **Pagination Support**: Manual and automatic pagination for large result sets (5000+ items)
- 🚦 **Rate Limit Management**: Transparent retry handling with configurable backoff strategies
- 🔍 **Advanced Filtering**: Chain filtering, DeFi positions, spam filtering, transaction types, and more
- 🧪 **Testnet Support**: Test applications on testnets (Sepolia, Monad, etc.) via X-Env header
- 💱 **Multi-Currency**: Portfolio values in USD, ETH, EUR, or BTC denomination
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

## Pagination - Fetching Large Result Sets

The Zerion API uses cursor-based pagination for endpoints that return lists (transactions, positions, NFTs). The MCP server provides both manual and automatic pagination support.

### Why Pagination Matters

Active wallets can have **thousands of transactions**. Without pagination:
- API quota exhausted quickly (Developer tier: ~5K requests/day)
- Incomplete data (default page size: 100 items)
- Slow responses (large payloads)

### Manual Pagination

All list endpoints support `page[size]` and `page[after]` parameters:

```
Use listWalletTransactions with:
- address: "0x..."
- page[size]: 100
- filter[trash]: "only_non_trash"
```

The response includes a `links.next` URL for fetching the next page:

```json
{
  "data": [...],
  "links": {
    "next": "https://api.zerion.io/v1/wallets/.../transactions?page[after]=cursor123"
  }
}
```

**To fetch the next page**, extract the cursor from `links.next` and use it as `page[after]`:

```
Use listWalletTransactions with:
- address: "0x..."
- page[size]: 100
- page[after]: "cursor123"
```

Continue until `links.next` is absent (last page reached).

### Automatic Pagination (Python SDK)

For programmatic access, use the auto-pagination helper to fetch all pages automatically:

```python
from zerion_mcp_server.pagination import fetch_all_pages
from zerion_mcp_server import RetryAsyncClient

# Create client
client = RetryAsyncClient(
    base_url="https://api.zerion.io",
    headers={"Authorization": "Bearer your-key"}
)

# Define your API call
async def get_transactions(address, **kwargs):
    response = await client.get(
        f"/v1/wallets/{address}/transactions",
        params=kwargs
    )
    return response.json()

# Fetch all transactions (up to max_pages)
all_transactions = await fetch_all_pages(
    api_call=lambda **kw: get_transactions("0x123...", **kw),
    max_pages=50,  # Safety limit
    page_size=100
)

print(f"Total transactions: {len(all_transactions)}")
```

### Pagination Configuration

Control pagination behavior in `config.yaml`:

```yaml
pagination:
  # Default page size (max: 100)
  default_page_size: 100

  # Safety limit for auto-pagination
  max_auto_pages: 50
```

**Example calculations**:
- 50 pages × 100 items = 5,000 results (covers 99% of wallets)
- 50 API requests consumed (watch your quota!)

### Pagination Best Practices

#### 1. Use Filters to Reduce Results

**Bad** (fetches everything):
```
listWalletTransactions:
  - address: "0x..."
  - page[size]: 100
```
**Result**: 2,000 transactions (20 pages)

**Good** (filter first):
```
listWalletTransactions:
  - address: "0x..."
  - filter[chain_ids]: "ethereum"
  - filter[trash]: "only_non_trash"
  - page[size]: 100
```
**Result**: 300 transactions (3 pages) - 85% quota savings!

#### 2. Choose Appropriate Page Sizes

- **Small pages (25-50)**: Faster individual requests, more total requests
- **Large pages (100)**: Fewer requests, larger payloads (recommended)
- **Default**: 100 items per page

#### 3. Monitor Auto-Pagination Limits

The auto-pagination helper logs warnings at key thresholds:

```
INFO: Fetched 10 pages - quota impact may be significant
WARNING: Fetched 25 pages - high quota usage
WARNING: Reached max page limit (50) - results may be incomplete
```

If you see "results may be incomplete", increase `max_auto_pages` or use manual pagination.

### Quota Impact Example

**Scenario**: Fetch all transactions for an active wallet (5,000 transactions)

| Approach | Requests | Quota Impact (Developer Tier) |
|----------|----------|-------------------------------|
| Manual (1 page) | 1 | ~0.02% of daily quota |
| Auto-paginate (50 pages) | 50 | ~1% of daily quota |
| Without filters (200 pages) | 200 | ~4% of daily quota |

**Takeaway**: Use filters + reasonable `max_pages` limits to avoid quota exhaustion.

---

## Rate Limiting - Automatic Retry with Backoff

The Zerion API enforces rate limits based on your subscription tier:

| Tier | Rate Limit | Daily Requests | Price |
|------|------------|----------------|-------|
| **Developer** (free) | 2 RPS | ~5,000/day | $0 |
| **Builder** | 50 RPS | ~500,000/day | $149/mo |
| **Pro** | 150 RPS | ~1.5M/day | $599/mo |
| **Enterprise** | Custom | Custom | Contact sales |

When you exceed your quota, the API returns `429 Too Many Requests` with a `Retry-After` header.

### Automatic Retry Behavior

The MCP server **automatically retries** rate-limited requests using exponential backoff with jitter:

```
Request → 429 (rate limit)
 ↓ Wait 1 second
Retry 1 → 429
 ↓ Wait 2 seconds (exponential backoff)
Retry 2 → 429
 ↓ Wait 4 seconds
Retry 3 → 200 OK (success!)
```

**You don't need to handle retries manually** - the server handles them transparently.

### Retry Configuration

Customize retry behavior in `config.yaml`:

```yaml
retry_policy:
  # Maximum retry attempts before raising error
  max_attempts: 5

  # Base delay for exponential backoff (seconds)
  base_delay: 1

  # Maximum delay between retries (seconds)
  max_delay: 60

  # Exponential backoff multiplier
  exponential_base: 2
```

**Delay sequence** (with exponential_base=2):
- Retry 1: 1 second
- Retry 2: 2 seconds
- Retry 3: 4 seconds
- Retry 4: 8 seconds
- Retry 5: 16 seconds

Total maximum wait: ~31 seconds (if all retries needed).

### Rate Limit Error Messages

If retries are exhausted, you'll see an actionable error:

```
RateLimitError: Rate limit exceeded after 5 retry attempts.
Retry after 60 seconds. Consider upgrading tier or reducing
request frequency. See: https://zerion.io/pricing
```

**Next steps**:
1. Wait for the `retry_after` duration (from error message)
2. Reduce request frequency in your app
3. Upgrade to a higher tier if needed

### Rate Limiting Best Practices

#### 1. Use Webhooks Instead of Polling

**Bad** (polling):
```python
# Check for new transactions every 10 seconds
while True:
    transactions = get_transactions(address)
    time.sleep(10)
```
**Cost**: 8,640 requests/day (exceeds Developer tier quota!)

**Good** (webhooks):
```python
# Webhook delivers new transactions as they happen
# 0 polling requests, only create subscription once
create_webhook_subscription(addresses=[address])
```
**Cost**: 1 request total 🎯

#### 2. Implement Client-Side Caching

```python
from functools import lru_cache
import time

@lru_cache(maxsize=100)
def get_portfolio(address, ttl_hash):
    return fetch_wallet_portfolio(address)

# Cache for 5 minutes
def get_ttl_hash(seconds=300):
    return round(time.time() / seconds)

# Usage
portfolio = get_portfolio(address, get_ttl_hash())
```

#### 3. Use Filters to Reduce Data Volume

Smaller responses = faster processing = fewer timeout retries:

```
Use listWalletTransactions with:
- filter[chain_ids]: "ethereum"
- filter[trash]: "only_non_trash"
- page[size]: 50
```

### Monitoring Rate Limit Status

The server logs rate limit events:

```
WARNING: Rate limit exceeded (url=/v1/wallets/.../transactions, retry_after=30s)
INFO: Retrying request after rate limit (attempt=2)
INFO: Request succeeded after 2 retry attempts
```

Enable **DEBUG** logging to see detailed retry information:

```yaml
logging:
  level: "DEBUG"
```

### Disabling Automatic Retry

To disable automatic retry (e.g., for testing):

```yaml
retry_policy:
  max_attempts: 0  # Disable retries
```

Now `429` responses will immediately raise `RateLimitError`.

---

## Error Handling - 202 Accepted (Wallet Indexing)

When you query a **newly created wallet** (first request for that address), Zerion may return `202 Accepted` instead of `200 OK`. This means:

> "Wallet is being indexed. Data will be ready in 2-10 seconds."

### Automatic 202 Retry

The MCP server **automatically retries** `202` responses with a fixed delay:

```
Request → 202 Accepted (indexing...)
 ↓ Wait 3 seconds
Retry 1 → 202 Accepted (still indexing...)
 ↓ Wait 3 seconds
Retry 2 → 200 OK (indexing complete!)
```

**You don't see `202` responses** - the server handles them transparently.

### When Does 202 Occur?

- **First request to a new wallet address**: Zerion hasn't indexed it yet
- **Recently created on-chain wallet**: Blockchain confirmed, Zerion indexing in progress
- **Rare edge case**: Heavy load on Zerion's indexing service

**Typical indexing time**: 2-10 seconds (usually 3-5 seconds).

### 202 Configuration

Customize retry behavior in `config.yaml`:

```yaml
wallet_indexing:
  # Delay between retries (seconds)
  retry_delay: 3

  # Maximum retry attempts
  max_retries: 3

  # Automatically retry (recommended: true)
  auto_retry: true
```

**Total wait time**: `retry_delay × max_retries` (e.g., 3s × 3 = 9 seconds).

### 202 Error Messages

If indexing times out after max retries:

```
WalletIndexingError: Wallet is still being indexed by Zerion.
Tried 3 times over 9 seconds. Please retry in 30-60 seconds.
```

**Next steps**:
1. Wait 30-60 seconds for Zerion to complete indexing
2. Retry your request
3. If issue persists, contact api@zerion.io

### Disabling 202 Auto-Retry

To disable automatic retry (e.g., for instant feedback):

```yaml
wallet_indexing:
  auto_retry: false
```

Now `202` responses will immediately raise:

```
WalletIndexingError: Wallet indexing in progress. This is a
new wallet address for Zerion. Enable auto_retry in
configuration or wait and retry manually.
```

### 202 Logging

The server logs indexing events:

```
INFO: Wallet indexing in progress, will retry (retry_delay=3s, max_retries=3)
INFO: Retrying wallet indexing request (attempt=1/3)
INFO: Wallet indexing completed successfully (attempts=2, total_wait=6s)
```

Or if timeout:

```
WARNING: Wallet indexing timeout (attempts=3, total_wait=9s)
```

### Troubleshooting 202 Errors

#### "Indexing timeout after 3 retries"

**Cause**: Wallet indexing taking longer than expected (>9 seconds).

**Solution**:
1. Increase `max_retries` or `retry_delay`:
   ```yaml
   wallet_indexing:
     retry_delay: 5
     max_retries: 5
   ```
   New total wait: 5s × 5 = 25 seconds

2. Wait 1-2 minutes and retry manually

#### "This is a new wallet address"

**Cause**: Normal behavior for first request to a wallet.

**Solution**: No action needed if `auto_retry: true` (default). The server will retry automatically.

---

## Testnet Support

Certain Zerion API endpoints support testnet data through the `X-Env` header parameter. This allows developers to test applications on testnets before deploying to mainnet.

### Supported Testnet Endpoints

The following endpoints accept the `X-Env` header:

- **`listWalletPositions`** - Get wallet positions on testnets
- **`getWalletPortfolio`** - Get portfolio data for testnet wallets
- **`listWalletTransactions`** - Fetch testnet transaction history
- **`listWalletNFTPositions`** - Get NFT positions on testnets
- **`listWalletNFTCollections`** - List NFT collections on testnets
- **`getWalletNftPortfolio`** - Get NFT portfolio for testnets
- **`listFungibles`** - List fungible assets on testnets
- **`getFungibleById`** - Get specific fungible on testnets
- **`listChains`** - List chains (including testnets)

### Using Testnet Data

To query testnet data, include `X-Env: testnet` when calling supported endpoints:

```
Use listWalletPositions with:
- address: "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"
- X-Env: "testnet"
- currency: "usd"
```

This will return positions for the specified address on testnet chains (e.g., Ethereum Sepolia, Monad Testnet).

### Testnet API Access

**Important**: Testnet access may require special API credentials or specific tier access. Check your API key capabilities:

- Contact api@zerion.io for testnet API access
- Verify your tier includes testnet support
- Some testnets may have limited data availability

### Testnet Development Workflow

**Recommended workflow for testnet-first development:**

1. **Create Test Wallet on Testnet** (e.g., Sepolia)
2. **Fund with Testnet Tokens** (use faucets)
3. **Test MCP Tools** with `X-Env: testnet`
4. **Verify Data Accuracy** on testnet
5. **Deploy to Mainnet** after validation

**Example - Testing Portfolio Fetch**:

```
# Test on Sepolia first
Use getWalletPortfolio with:
- address: "0x..."
- X-Env: "testnet"
- currency: "usd"

# Then move to mainnet
Use getWalletPortfolio with:
- address: "0x..."
- currency: "usd"
```

### Supported Testnet Chains

Use `listChains` with `X-Env: testnet` to see all available testnet chains. Common testnets include:

- **Ethereum Sepolia** (`sepolia`)
- **Monad Testnet** (`monad-testnet`)
- **Base Sepolia** (`base-sepolia`)
- **Optimism Sepolia** (`optimism-sepolia`)
- **Arbitrum Sepolia** (`arbitrum-sepolia`)

**Note**: Testnet chain availability may vary. Use the `listChains` endpoint to get the current list.

### Testnet Limitations

- **Data Freshness**: Testnet indexing may be slower than mainnet
- **Historical Data**: Some testnets have limited historical data
- **Protocol Coverage**: Not all DeFi protocols deployed on testnets
- **Price Data**: Testnet tokens typically have no market price

---

## Multi-Currency Support

The Zerion API supports multiple currencies for price denomination. You can request portfolio values, position prices, and charts in USD, ETH, EUR, or BTC.

### Supported Currencies

| Currency | Code | Use Case |
|----------|------|----------|
| **US Dollar** | `usd` | Default, most common for general users |
| **Ethereum** | `eth` | DeFi analytics, ETH-native communities |
| **Euro** | `eur` | European users, EU compliance requirements |
| **Bitcoin** | `btc` | Bitcoin-maximalist perspectives |

### Currency-Compatible Endpoints

The `currency` parameter is supported on these endpoints:

- **`getWalletPortfolio`** - Portfolio total value in specified currency
- **`listWalletPositions`** - Position values in specified currency
- **`getWalletChart`** - Historical balance chart in specified currency
- **`getWalletPNL`** - Profit/Loss calculations in specified currency
- **`getFungibleChart`** - Asset price charts in specified currency

### Using Different Currencies

**USD (Default)**:
```
Use getWalletPortfolio with:
- address: "0x..."
- currency: "usd"
```

**ETH Denomination**:
```
Use getWalletPortfolio with:
- address: "0x..."
- currency: "eth"
```

This returns portfolio value in ETH. For example, if a wallet is worth $10,000 and ETH is $2,000, the value would be shown as 5 ETH.

**EUR Denomination**:
```
Use listWalletPositions with:
- address: "0x..."
- currency: "eur"
- filter[chain_ids]: "ethereum"
```

All position values will be shown in EUR instead of USD.

**BTC Denomination**:
```
Use getWalletChart with:
- address: "0x..."
- currency: "btc"
- period: "month"
```

Historical portfolio values will be shown in BTC equivalent.

### Currency Parameter Behavior

**Default Behavior**: If `currency` parameter is omitted, USD is used by default.

**Price Fields Affected**: The currency parameter affects:
- `attributes.value` - Total value
- `attributes.price` - Individual asset prices
- `attributes.changes` - Value changes over time
- `attributes.floor_price` - NFT floor prices (where applicable)

**Exchange Rates**: Zerion uses real-time exchange rates for currency conversion. Rates are updated continuously.

### Multi-Currency Examples

**Example 1: DeFi Portfolio in ETH**
```
Use listWalletPositions with:
- address: "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
- filter[positions]: "only_complex"
- currency: "eth"
```

Result: All DeFi position values shown in ETH denomination.

**Example 2: European User Portfolio**
```
Use getWalletPortfolio with:
- address: "0x..."
- currency: "eur"
```

Result: Portfolio value and all asset prices in EUR.

**Example 3: Historical Performance in BTC**
```
Use getWalletChart with:
- address: "0x..."
- currency: "btc"
- period: "year"
```

Result: Year-long portfolio performance chart denominated in BTC.

### Currency Best Practices

1. **Use USD for General Applications** - Most users expect USD pricing
2. **Use ETH for DeFi Dashboards** - DeFi users often think in ETH terms
3. **Use EUR for EU Compliance** - Required for some European regulatory reporting
4. **Use BTC for Bitcoin Communities** - Aligns with Bitcoin-centric worldview

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
