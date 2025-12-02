# Zerion MCP Server - Use Cases & Applications

This document provides practical use cases for the Zerion MCP Server, demonstrating how to leverage its capabilities for various cryptocurrency analytics, portfolio management, and monitoring applications.

---

## Table of Contents

1. [Token Project Analytics Dashboard](#1-token-project-analytics-dashboard)
2. [DeFi Protocol Risk Monitoring](#2-defi-protocol-risk-monitoring)
3. [Whale Wallet Tracker](#3-whale-wallet-tracker)
4. [Multi-Chain Portfolio Aggregator](#4-multi-chain-portfolio-aggregator)
5. [NFT Collection Analytics](#5-nft-collection-analytics)
6. [Treasury Management Dashboard](#6-treasury-management-dashboard)
7. [Trading Analytics & Performance Tracking](#7-trading-analytics--performance-tracking)
8. [Real-Time Transaction Monitoring](#8-real-time-transaction-monitoring)
9. [Tax Reporting & PnL Analysis](#9-tax-reporting--pnl-analysis)
10. [Cross-Chain Yield Optimizer](#10-cross-chain-yield-optimizer)

---

## 1. Token Project Analytics Dashboard

### Overview
Monitor key metrics for a cryptocurrency project including token price, known holder positions, profit/loss analysis, and transaction activity.

### What You Can Track

#### Token Metadata & Market Data
- **Contract address** and deployment details
- **Token symbol, name, and decimals**
- **Current price** across multiple currencies (USD, ETH, EUR, BTC)
- **Historical price charts** (day, week, month, year, all-time)
- **Chain information** (which networks the token is deployed on)

#### Known Holder Analysis
Monitor wallets you've identified (team, investors, VCs, known whales):
- **Portfolio value** for each holder
- **Position size** (token balance) for specific holders
- **Profit & Loss (PnL)** calculations per holder
- **Transaction history** (buys, sells, transfers)
- **DeFi positions** (staking, LP, lending) involving the token

### Important Limitation

**The Zerion API is wallet-centric, not token-centric.** This means:
- ❌ You **CANNOT** discover all holders of a token
- ❌ You **CANNOT** get a "top 100 holders" list directly from Zerion
- ✅ You **CAN** track specific wallet addresses you already know
- ✅ You **CAN** get token metadata and price information

### Solution Architecture

```
┌─────────────────────┐
│  External Data      │  (Etherscan, Dune, on-chain indexers)
│  Source             │  → Discover holder addresses
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Holder Address     │  (Your curated list)
│  Database           │  → Team: 0xABC...
└──────────┬──────────┘  → VC Fund: 0xDEF...
           │             → Whale 1: 0x123...
           ▼
┌─────────────────────┐
│  Zerion MCP Server  │
│                     │
│  For each holder:   │
│  - getWalletPortfolio
│  - listWalletPositions (filter by token)
│  - getWalletPNL
│  - listWalletTransactions
└─────────────────────┘
```

### Implementation Example

```markdown
## Step 1: Get Token Information

Use getFungibleById with:
- fungible_id: "ethereum:0x1f9840a85d5af5bf1d1762f925bdaddc4201f984"  # UNI token
- currency: "usd"

Returns:
- Contract address: 0x1f9840a85d5af5bf1d1762f925bdaddc4201f984
- Symbol: UNI
- Name: Uniswap
- Current price: $8.45
- Chain: Ethereum

## Step 2: Get Token Price Chart

Use getFungibleChart with:
- fungible_id: "ethereum:0x1f9840a85d5af5bf1d1762f925bdaddc4201f984"
- chart_period: "month"
- currency: "usd"

Returns: 30-day price history

## Step 3: Monitor Known Holders

### Holder 1: Team Wallet (0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045)

Use listWalletPositions with:
- address: "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
- filter[fungible_ids]: "ethereum:0x1f9840a85d5af5bf1d1762f925bdaddc4201f984"
- filter[trash]: "only_non_trash"
- currency: "usd"

Returns: Position size, current value, locked/staked amounts

Use getWalletPNL with:
- address: "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
- filter[fungible_ids]: "ethereum:0x1f9840a85d5af5bf1d1762f925bdaddc4201f984"

Returns: Realized PnL, Unrealized PnL, cost basis

Use listWalletTransactions with:
- address: "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
- filter[fungible_ids]: "ethereum:0x1f9840a85d5af5bf1d1762f925bdaddc4201f984"
- filter[operation_types]: "trade,transfer"
- page[size]: 50

Returns: Recent buys, sells, transfers

### Holder 2: VC Fund Wallet (0x...)
[Repeat same queries for each known holder]
```

### Dashboard Metrics

| Metric | Data Source | MCP Tool |
|--------|-------------|----------|
| **Token Price** | Real-time price | `getFungibleById` |
| **24h Price Change** | Price chart | `getFungibleChart` (1d period) |
| **Holder Balance** | Wallet positions | `listWalletPositions` + filter |
| **Holder PnL** | Profit/Loss calc | `getWalletPNL` + filter |
| **Recent Transactions** | Tx history | `listWalletTransactions` + filter |
| **Locked/Staked Amount** | DeFi positions | `listWalletPositions` (only_complex) |

### Recommended External Data Sources for Holder Discovery

Since Zerion doesn't provide holder discovery, combine it with:
- **Etherscan API**: Top token holders list
- **Dune Analytics**: Custom SQL queries for holders
- **On-chain indexers**: The Graph, Moralis, Alchemy
- **Manual research**: Team addresses from documentation, VC announcements

### Real-World Example: Monitoring UNI Token

```yaml
Project: Uniswap (UNI Token)
Token ID: ethereum:0x1f9840a85d5af5bf1d1762f925bdaddc4201f984

Known Holders to Monitor:
  - Uniswap Treasury: 0x1a9C8182C09F50C8318d769245beA52c32BE35BC
  - a16z Fund: 0x...
  - Jump Trading: 0x...
  - Binance Hot Wallet: 0x...

Metrics Tracked:
  1. UNI price (USD, ETH)
  2. Each holder's UNI balance
  3. Each holder's PnL on UNI
  4. Recent UNI transfers (alerts for large moves)
  5. UNI staked in governance
  6. UNI used in LP positions (Uniswap V3 pools)

Update Frequency:
  - Price: Real-time via webhooks or 5-min polling
  - Balances: Hourly
  - Transactions: Webhook-based (instant notifications)
```

---

## 2. DeFi Protocol Risk Monitoring

### Overview
Track exposure to specific DeFi protocols across multiple wallets to manage risk, monitor yields, and detect protocol issues.

### Key Capabilities

- **Protocol-specific filtering**: `filter[dapp_ids]` to isolate specific protocols
- **Position categorization**: Deposits, loans, staked, LP positions, rewards
- **Multi-chain aggregation**: Track protocol positions across all chains
- **Real-time alerts**: Webhook notifications for position changes

### Implementation

```markdown
## Monitor Aave V3 Exposure Across Portfolio

Use listWalletPositions with:
- address: "0x..."
- filter[dapp_ids]: "aave-v3"
- filter[positions]: "only_complex"
- currency: "usd"
- filter[chain_ids]: "ethereum,polygon,base,optimism"

Returns:
- All Aave V3 deposits (supplied assets)
- All Aave V3 loans (borrowed assets)
- Health factor metadata
- Interest earned (rewards)

## Calculate Total Protocol Exposure

1. Query each wallet in portfolio
2. Filter for target protocol (e.g., "curve", "lido", "compound-v2")
3. Aggregate total value locked
4. Calculate risk metrics:
   - Borrowed vs. collateral ratio
   - Single protocol concentration (%)
   - Yield APY across all positions
```

### Dashboard Example: Multi-Protocol Risk

| Protocol | Total Value | Position Types | Chains | Alerts |
|----------|-------------|----------------|--------|--------|
| **Aave V3** | $125,000 | Deposit: $100k, Loan: $25k | ETH, Base, Polygon | Health Factor: 2.1 ✅ |
| **Curve** | $80,000 | LP: $80k | Ethereum | IL Risk: Moderate ⚠️ |
| **Lido** | $250,000 | Staked: $250k | Ethereum | Staking APY: 3.2% ✅ |
| **Uniswap V3** | $45,000 | LP: $45k | ETH, Arbitrum | Out-of-range: 1 pool ⚠️ |

### Use Cases

- **Institutional treasury management**: Monitor DAO treasury DeFi positions
- **Hedge fund risk**: Track protocol concentration risk
- **Smart contract audits**: Monitor deposits after protocol upgrades
- **Yield farming**: Compare yields across protocols

---

## 3. Whale Wallet Tracker

### Overview
Monitor activities of influential crypto wallets (whales, VCs, smart money) to identify trends, trading patterns, and early signals.

### Key Features

- **Portfolio snapshots**: Track total holdings over time
- **Transaction monitoring**: Real-time alerts for whale trades
- **Multi-chain tracking**: Follow whales across 100+ blockchains
- **PnL analysis**: Calculate whale profitability

### Implementation

```markdown
## Whale Watchlist Setup

Whale 1: a16z Fund
  - Address: 0x...
  - Focus: Ethereum, Base (L2 bets)
  - Alert triggers: Trades > $1M, new token positions

Whale 2: Jump Trading
  - Address: 0x...
  - Focus: Arbitrage, high-frequency
  - Alert triggers: Any transaction

Whale 3: Alameda Research Archive
  - Address: 0x...
  - Focus: Historical analysis
  - Alert triggers: None (research only)

## Monitor Whale Activity

### Daily Portfolio Snapshot

Use getWalletPortfolio with:
- address: "0x..." (whale address)
- currency: "usd"

Track over time:
- Total portfolio value
- 24h change %
- Changes.absolute_1d (daily P&L)

### Recent Transactions

Use listWalletTransactions with:
- address: "0x..."
- filter[trash]: "only_non_trash"
- filter[operation_types]: "trade"
- page[size]: 100
- sort: "-mined_at" (newest first)

Alert on:
- Large trades (> $100k)
- New token purchases (potential alpha)
- Token sales (exit signals)

### Position Changes

Use listWalletPositions with:
- address: "0x..."
- filter[trash]: "only_non_trash"
- currency: "usd"
- sort: "value" (largest first)

Track:
- New positions (potential trends)
- Exited positions (risk signals)
- Position size changes (conviction signals)

## Real-Time Monitoring

Use createTxSubscription with:
- addresses: ["0x...", "0x...", "0x..."] (all whales)
- callback_url: "https://your-server.com/webhooks/whale-alerts"
- chain_ids: ["ethereum", "base", "arbitrum"]

Webhook triggers:
- Instant notifications for whale transactions
- No polling required (conserves quota)
- Process and alert via Telegram/Discord/Slack
```

### Analysis Patterns

**Smart Money Flow**:
1. Track 10-20 known "smart money" wallets
2. Identify common token purchases within 7-day window
3. Research tokens with 3+ whale buyers (potential alpha)

**Exit Signals**:
1. Monitor whale positions for your holdings
2. Alert if 2+ whales reduce position by >20%
3. Consider de-risking your own position

**New Trend Discovery**:
1. Track whales known for early bets (VCs, successful traders)
2. Alert on new DeFi protocol deposits
3. Research new protocols with whale capital inflow

---

## 4. Multi-Chain Portfolio Aggregator

### Overview
Unified portfolio view across 100+ blockchain networks, eliminating the need for multiple block explorers and chain-specific tools.

### Key Features

- **Automatic aggregation**: Single API call returns all chains
- **Chain-specific filtering**: Focus on specific ecosystems
- **Multi-currency support**: View in USD, ETH, EUR, BTC
- **Historical tracking**: Portfolio value over time across all chains

### Implementation

```markdown
## Complete Portfolio View

Use getWalletPortfolio with:
- address: "0x..."
- currency: "usd"

Returns: Total value across ALL chains (Ethereum, Base, Polygon, Arbitrum, Solana, etc.)

Example response:
- Total value: $485,234
- 24h change: +$12,450 (+2.64%)
- Chains with balances: 12
  - Ethereum: $350,000
  - Base: $85,000
  - Arbitrum: $30,000
  - Polygon: $15,234
  - etc.

## L2 Ecosystem Focus

Use listWalletPositions with:
- address: "0x..."
- filter[chain_ids]: "base,optimism,arbitrum"
- filter[trash]: "only_non_trash"
- currency: "usd"

Returns: Only positions on Layer 2 networks

Use case: Compare L2 holdings vs. Ethereum mainnet

## Mainnet vs. L2 Comparison

Query 1: Ethereum only
  filter[chain_ids]: "ethereum"

Query 2: All L2s
  filter[chain_ids]: "base,optimism,arbitrum,polygon,zksync"

Analysis:
- Calculate % of portfolio on L2 vs. mainnet
- Identify migration patterns
- Gas cost savings analysis
```

### Dashboard Example

```
╔══════════════════════════════════════════════════════════╗
║         MULTI-CHAIN PORTFOLIO DASHBOARD                  ║
╠══════════════════════════════════════════════════════════╣
║  Total Value: $485,234                                   ║
║  24h Change: +$12,450 (+2.64%)                          ║
╠══════════════════════════════════════════════════════════╣
║  CHAIN BREAKDOWN                                         ║
╠══════════════════════════════════════════════════════════╣
║  🟦 Ethereum        $350,000  (72.1%)  ████████████████ ║
║  🔵 Base            $ 85,000  (17.5%)  ████             ║
║  🔴 Arbitrum        $ 30,000  ( 6.2%)  █               ║
║  🟣 Polygon         $ 15,234  ( 3.1%)  █               ║
║  ⚫ Solana          $  5,000  ( 1.0%)                   ║
╠══════════════════════════════════════════════════════════╣
║  TOP POSITIONS (ALL CHAINS)                              ║
╠══════════════════════════════════════════════════════════╣
║  1. ETH (staked)    $180,000  Ethereum   [Lido]         ║
║  2. WETH            $ 95,000  Ethereum                   ║
║  3. USDC            $ 75,000  Multi-chain                ║
║  4. UNI (LP)        $ 45,000  Base       [Uniswap V3]   ║
║  5. AAVE (deposit)  $ 30,000  Ethereum   [Aave V3]      ║
╚══════════════════════════════════════════════════════════╝
```

---

## 5. NFT Collection Analytics

### Overview
Track NFT portfolios, collection floor prices, and individual NFT metadata across multiple wallets and chains.

### Key Features

- **Collection-level aggregation**: View holdings by collection
- **Floor price tracking**: Monitor collection valuations
- **Metadata completeness**: Images, traits, descriptions
- **Spam filtering**: Hide spam/scam NFT airdrops

### Implementation

```markdown
## NFT Portfolio Overview

Use getWalletNftPortfolio with:
- address: "0x..."
- filter[trash]: "only_non_trash"
- currency: "usd"

Returns:
- Total NFT portfolio value
- Number of NFTs held
- Number of collections
- Floor price valuations

## List NFT Collections

Use listWalletNFTCollections with:
- address: "0x..."
- filter[trash]: "only_non_trash"

Returns:
- Collection names
- Number of NFTs owned per collection
- Floor prices
- Total collection value

## Individual NFT Details

Use listWalletNFTPositions with:
- address: "0x..."
- filter[trash]: "only_non_trash"
- page[size]: 100

Returns: List of individual NFTs with:
- metadata.name
- metadata.description
- metadata.content.preview (thumbnail URL)
- metadata.content.detail (high-res URL)
- market_data.prices.floor
- metadata.attributes (traits)

## Monitor Specific NFT

Use getNFTById with:
- nft_id: "ethereum:0x74ee68a33f6c9f113e22b3b77418b75f85d07d22:10"
- currency: "usd"

Returns: Complete metadata for single NFT
```

### Use Cases

**NFT Gallery App**:
- Display user's NFT collection with images
- Show floor prices and estimated values
- Filter by collection or chain
- Hide spam NFTs automatically

**Collection Floor Price Alerts**:
1. Track floor price for owned collections
2. Alert if floor drops > 20% (exit signal)
3. Alert if floor increases > 50% (sell opportunity)

**Blue-Chip NFT Tracker**:
- Monitor holdings of BAYC, CryptoPunks, Azuki, etc.
- Track total value in blue-chip NFTs vs. speculative
- Risk analysis: diversification across collections

---

## 6. Treasury Management Dashboard

### Overview
DAOs and protocols can monitor treasury holdings across multiple chains, track expenses, and analyze treasury health.

### Key Features

- **Multi-chain treasury tracking**: Aggregate across all chains
- **DeFi yield positions**: Monitor treasury staking/lending
- **Transaction categorization**: Track inflows/outflows
- **Historical performance**: Treasury value over time

### Implementation

```markdown
## DAO Treasury Overview

Treasury Address: 0x1a9C8182C09F50C8318d769245beA52c32BE35BC (Uniswap)

Use getWalletPortfolio with:
- address: "0x1a9C8182C09F50C8318d769245beA52c32BE35BC"
- currency: "usd"

Returns:
- Total treasury value
- 30-day change
- Asset breakdown

## Treasury Asset Breakdown

Use listWalletPositions with:
- address: "0x1a9C8182C09F50C8318d769245beA52c32BE35BC"
- filter[trash]: "only_non_trash"
- currency: "usd"
- sort: "value"

Categorize by:
- Stablecoins (USDC, DAI, USDT) → Operating runway
- Native tokens (UNI) → Long-term reserves
- DeFi positions → Yield-generating assets
- Other tokens → Diversification

## Treasury DeFi Positions

Use listWalletPositions with:
- address: "0x1a9C8182C09F50C8318d769245beA52c32BE35BC"
- filter[positions]: "only_complex"
- currency: "usd"

Track:
- Staking positions (ETH staking via Lido)
- Lending positions (USDC lent on Aave)
- LP positions (Treasury market-making)
- Locked tokens (Vesting schedules)

## Treasury Expense Tracking

Use listWalletTransactions with:
- address: "0x1a9C8182C09F50C8318d769245beA52c32BE35BC"
- filter[operation_types]: "transfer"
- filter[trash]: "only_non_trash"
- page[size]: 100

Analyze:
- Outgoing transfers (expenses)
- Incoming transfers (revenue, grants)
- Calculate monthly burn rate
- Project runway (months of expenses remaining)

## Historical Treasury Value

Use getWalletChart with:
- address: "0x1a9C8182C09F50C8318d769245beA52c32BE35BC"
- period: "year"
- currency: "usd"

Track:
- Treasury growth over time
- Impact of major events
- Diversification effectiveness
```

### Treasury Metrics Dashboard

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| **Total Value** | $42.5M | - | - |
| **Stablecoins** | $15.2M | >$10M | ✅ |
| **Monthly Burn** | $850K | <$1M | ✅ |
| **Runway** | 18 months | >12 months | ✅ |
| **Yield Generated** | $125K/mo | >$100K | ✅ |
| **Native Token %** | 48% | <60% | ✅ |

---

## 7. Trading Analytics & Performance Tracking

### Overview
Analyze trading behavior, calculate win rates, identify profitable strategies, and track performance across DEX trades.

### Key Features

- **Trade history filtering**: Isolate swaps from other transactions
- **PnL calculations**: Realized and unrealized gains
- **Multi-DEX aggregation**: Track trades across Uniswap, Curve, 1inch, etc.
- **Performance metrics**: Win rate, average profit, largest trades

### Implementation

```markdown
## Get All Trades (DEX Swaps)

Use listWalletTransactions with:
- address: "0x..."
- filter[operation_types]: "trade"
- filter[trash]: "only_non_trash"
- filter[chain_ids]: "ethereum,base,arbitrum"
- page[size]: 100

Returns: Only DEX swap transactions

## Analyze Trade Performance

Use getWalletPNL with:
- address: "0x..."
- currency: "usd"

Returns:
- attributes.realized_pnl.value → Realized gains/losses
- attributes.unrealized_pnl.value → Unrealized (open positions)
- attributes.cost_basis.value → Total invested

Calculate:
- Total ROI: (Realized + Unrealized) / Cost Basis
- Win rate: Count profitable vs. unprofitable trades
- Average trade size
- Largest win/loss

## Trading Frequency Analysis

Query transactions for last 30 days:
- Count total trades
- Calculate avg trades per day
- Identify most-traded tokens
- Identify preferred DEXs (Uniswap, Curve, etc.)

## Token-Specific Trading Performance

Use getWalletPNL with:
- address: "0x..."
- filter[fungible_ids]: "ethereum:0x..." (specific token)

Returns: PnL for that token only

Repeat for each major token traded to identify:
- Most profitable tokens
- Worst performing tokens
- Tokens to avoid
```

### Trading Dashboard Example

```
╔═══════════════════════════════════════════════════════════╗
║              TRADING PERFORMANCE DASHBOARD                 ║
╠═══════════════════════════════════════════════════════════╣
║  Period: Last 30 Days                                      ║
║  Total Trades: 47                                          ║
║  Win Rate: 68% (32 wins, 15 losses)                       ║
╠═══════════════════════════════════════════════════════════╣
║  PERFORMANCE                                               ║
╠═══════════════════════════════════════════════════════════╣
║  Realized PnL:     +$12,450                               ║
║  Unrealized PnL:   +$3,200                                ║
║  Total ROI:        +15.8%                                 ║
║  Avg Trade Size:   $5,250                                 ║
╠═══════════════════════════════════════════════════════════╣
║  TOP PERFORMERS                                            ║
╠═══════════════════════════════════════════════════════════╣
║  1. ETH → USDC     +$4,500  (12 trades, 83% win rate)    ║
║  2. WBTC → ETH     +$3,200  (5 trades, 100% win rate)    ║
║  3. UNI → USDC     +$2,100  (8 trades, 75% win rate)     ║
╠═══════════════════════════════════════════════════════════╣
║  WORST PERFORMERS                                          ║
╠═══════════════════════════════════════════════════════════╣
║  1. PEPE → ETH     -$1,800  (15 trades, 20% win rate)    ║
║  2. SHIB → USDC    -$950    (7 trades, 29% win rate)     ║
╠═══════════════════════════════════════════════════════════╣
║  PREFERRED DEXs                                            ║
╠═══════════════════════════════════════════════════════════╣
║  Uniswap V3:  32 trades (68%)                             ║
║  Curve:       10 trades (21%)                             ║
║  1inch:       5 trades (11%)                              ║
╚═══════════════════════════════════════════════════════════╝
```

---

## 8. Real-Time Transaction Monitoring

### Overview
Use webhooks to receive instant notifications when monitored wallets execute transactions, enabling real-time alerting and automated responses.

### Key Features

- **Sub-second latency**: Receive notifications within seconds of on-chain confirmation
- **Chain filtering**: Monitor specific blockchains only
- **Zero polling**: Webhooks push updates (conserves API quota)
- **Scalable**: Monitor hundreds of wallets simultaneously

### Implementation

```markdown
## Set Up Webhook Subscription

Use createTxSubscription with:
- addresses: [
    "0x...",  # Your wallet
    "0x...",  # Treasury wallet
    "0x...",  # Team wallet
    "0x..."   # Whale wallet to monitor
  ]
- callback_url: "https://your-server.com/webhooks/zerion"
- chain_ids: ["ethereum", "base", "arbitrum"]

Result: Subscription ID returned, webhooks will now be sent

## Process Webhook Payloads

When transaction occurs, Zerion POSTs to your callback_url:

{
  "data": {
    "attributes": {
      "address": "0x...",
      "timestamp": "2025-12-01T10:56:50Z"
    }
  },
  "included": [{
    "type": "transactions",
    "attributes": {
      "operation_type": "trade",
      "hash": "0x...",
      "status": "confirmed",
      "transfers": [...]
    },
    "relationships": {
      "chain": { "id": "ethereum" },
      "dapp": { "id": "uniswap-v3" }
    }
  }]
}

## Automated Alerting Logic

Process each webhook:
1. Extract transaction details
2. Apply business logic:
   - If operation_type == "trade" AND value > $10,000
     → Send Telegram alert "Large trade detected"
   - If operation_type == "transfer" AND direction == "outgoing"
     → Alert "Funds leaving monitored wallet"
   - If dapp == "uniswap-v3" AND new_token_position
     → Research alert "Whale bought new token"

## Use Cases

- **Security monitoring**: Alert on unauthorized transactions
- **Treasury oversight**: Notify on large outflows
- **Whale watching**: Get instant whale trade alerts
- **Smart contract triggers**: Execute automated actions on-chain
```

### Alert Types by Use Case

| Use Case | Alert Trigger | Action |
|----------|---------------|--------|
| **Security** | Any unexpected transaction | SMS + Email alert, freeze hot wallet |
| **Treasury** | Outflow > $50K | Notify treasury committee |
| **Whale Tracking** | Whale buys new token | Research token, send Discord notification |
| **Portfolio** | Position value drop > 10% | Risk management alert |
| **Compliance** | Any transaction from compliance wallet | Log for audit trail |

### Webhook Infrastructure

**Development/Testing**:
- Use webhook.site for instant testing
- No code required, just paste URL

**Production**:
- Deploy Flask/Express webhook receiver
- Use HTTPS (required by Zerion)
- Implement idempotency (handle duplicate deliveries)
- Process async (respond < 5 seconds)
- Queue heavy processing (Celery, Bull, etc.)

---

## 9. Tax Reporting & PnL Analysis

### Overview
Generate accurate tax reports by calculating realized gains, cost basis, and transaction history with FIFO methodology.

### Key Features

- **FIFO cost basis**: Automatically calculated by Zerion
- **Realized vs. Unrealized PnL**: Separate sold vs. held positions
- **Transaction categorization**: Differentiate trades, transfers, DeFi yields
- **Multi-currency**: Report in any supported currency

### Implementation

```markdown
## Annual Tax Report Generation

### Step 1: Get Overall PnL

Use getWalletPNL with:
- address: "0x..."
- currency: "usd"

Returns:
- attributes.realized_pnl.value → Capital gains (taxable)
- attributes.unrealized_pnl.value → Unrealized (not taxable until sold)
- attributes.cost_basis.value → Total invested
- attributes.invested_not_sold.value → Still holding (cost basis)
- attributes.transfers_in.value → Received from others (gift income?)
- attributes.transfers_out.value → Sent to others (gift tax?)

### Step 2: Get All Transactions (Tax Year)

Use listWalletTransactions with:
- address: "0x..."
- filter[trash]: "only_non_trash"
- page[size]: 100
- Auto-paginate to get all transactions

Filter client-side for tax year (e.g., 2024-01-01 to 2024-12-31)

### Step 3: Categorize Transactions

For each transaction, categorize:
- **Taxable Events**:
  - Trades (swap X for Y) → Capital gain/loss
  - DeFi yield claimed → Income
  - NFT sales → Capital gain/loss
  - Staking rewards → Income

- **Non-Taxable** (jurisdiction dependent):
  - Transfers between own wallets
  - Failed transactions
  - Approvals

### Step 4: Calculate Per-Token PnL

For each token sold:

Use getWalletPNL with:
- address: "0x..."
- filter[fungible_ids]: "ethereum:0x..." (specific token)

Returns: FIFO-calculated gains for that token

### Step 5: Generate Tax Forms

Export data in format required by jurisdiction:
- IRS Form 8949 (USA)
- UK HMRC Crypto Assets Manual
- Etc.

Include:
- Date acquired
- Date sold
- Cost basis (FIFO)
- Sale proceeds
- Gain/loss
- Holding period (short-term vs. long-term)
```

### Tax Report Dashboard

```
╔══════════════════════════════════════════════════════════╗
║           2024 CRYPTOCURRENCY TAX REPORT                  ║
╠══════════════════════════════════════════════════════════╣
║  Reporting Period: 2024-01-01 to 2024-12-31              ║
║  Wallet: 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045       ║
╠══════════════════════════════════════════════════════════╣
║  CAPITAL GAINS SUMMARY                                    ║
╠══════════════════════════════════════════════════════════╣
║  Realized Gains (Sold):        +$45,230                  ║
║  Unrealized Gains (Holding):   +$23,100 (not taxable)   ║
║  Total Transactions:            487                       ║
║  Taxable Events:                156                       ║
╠══════════════════════════════════════════════════════════╣
║  INCOME (DeFi Yields & Staking)                          ║
╠══════════════════════════════════════════════════════════╣
║  Staking Rewards:              $3,450                    ║
║  Lending Interest (Aave):      $1,230                    ║
║  LP Fees (Uniswap):            $890                      ║
║  Total DeFi Income:            $5,570                    ║
╠══════════════════════════════════════════════════════════╣
║  HOLDING PERIOD BREAKDOWN                                 ║
╠══════════════════════════════════════════════════════════╣
║  Short-Term (<1 year):         $12,450 gain              ║
║  Long-Term (>1 year):          $32,780 gain              ║
╠══════════════════════════════════════════════════════════╣
║  ESTIMATED TAX LIABILITY (USA)                           ║
╠══════════════════════════════════════════════════════════╣
║  Short-Term (37% rate):        $4,607                    ║
║  Long-Term (20% rate):         $6,556                    ║
║  Income (37% rate):            $2,061                    ║
║  Total Tax Due:                $13,224                   ║
╚══════════════════════════════════════════════════════════╝
```

### Important Notes

**Limitations**:
- Zerion provides FIFO cost basis calculations
- Tax rules vary by jurisdiction (consult tax professional)
- Some DeFi operations may not be captured correctly
- Consider using specialized crypto tax software (CoinTracker, Koinly) that integrates with Zerion data

**Best Practices**:
- Export transaction data monthly (easier than annual bulk export)
- Keep records of transfers between own wallets (to prove no taxable event)
- Document cost basis for tokens received as gifts/airdrops
- Track gas fees (may be deductible)

---

## 10. Cross-Chain Yield Optimizer

### Overview
Identify best yield opportunities across 100+ blockchains by comparing DeFi protocol APYs, calculating net yields after gas fees, and tracking performance.

### Key Features

- **Multi-chain DeFi discovery**: Find yield across all chains
- **Protocol comparison**: Compare Aave on Ethereum vs. Polygon
- **Position tracking**: Monitor existing yield positions
- **ROI calculation**: Track actual returns vs. projected APY

### Implementation

```markdown
## Discovery: Find All DeFi Positions

Use listWalletPositions with:
- address: "0x..."
- filter[positions]: "only_complex"
- filter[trash]: "only_non_trash"
- currency: "usd"

Returns all DeFi positions across all chains:
- Staking positions (with APY metadata if available)
- Lending deposits (Aave, Compound)
- LP positions (Uniswap, Curve)
- Yield farms (Yearn, Beefy)

## Chain-Specific Yield Comparison

### Ethereum Mainnet DeFi

Use listWalletPositions with:
- filter[chain_ids]: "ethereum"
- filter[positions]: "only_complex"

### L2 DeFi (Lower Gas Fees)

Use listWalletPositions with:
- filter[chain_ids]: "base,optimism,arbitrum,polygon"
- filter[positions]: "only_complex"

Compare:
- Similar protocols on different chains
- Net APY after gas costs
- TVL and liquidity depth

## Protocol-Specific Analysis

### Compare Aave Across Chains

Ethereum:
  - filter[chain_ids]: "ethereum"
  - filter[dapp_ids]: "aave-v3"

Polygon:
  - filter[chain_ids]: "polygon"
  - filter[dapp_ids]: "aave-v3"

Base:
  - filter[chain_ids]: "base"
  - filter[dapp_ids]: "aave-v3"

Analyze:
- Interest rates (supply APY)
- Borrowing costs
- Incentive programs (token rewards)
- Gas costs for deposits/withdrawals

## Historical Performance Tracking

Use getWalletChart with:
- address: "0x..."
- period: "month"
- currency: "usd"

Track portfolio value growth to measure actual yield vs. projected

Calculate:
- Actual APY = (End Value - Start Value - Net Deposits) / Start Value
- Compare to protocol advertised APY
- Identify best-performing strategies
```

### Yield Comparison Dashboard

```
╔══════════════════════════════════════════════════════════╗
║         CROSS-CHAIN YIELD OPPORTUNITIES                   ║
╠══════════════════════════════════════════════════════════╣
║  USDC Lending Comparison (Supply APY)                    ║
╠══════════════════════════════════════════════════════════╣
║  Protocol        Chain      APY    Gas Cost   Net APY    ║
╠══════════════════════════════════════════════════════════╣
║  Aave V3         Base       4.8%   ~$0.10     4.80%  ⭐  ║
║  Aave V3         Ethereum   4.5%   ~$15       4.35%      ║
║  Compound V2     Ethereum   3.9%   ~$20       3.70%      ║
║  Aave V3         Polygon    4.2%   ~$0.50     4.18%      ║
╠══════════════════════════════════════════════════════════╣
║  ETH Staking Comparison                                   ║
╠══════════════════════════════════════════════════════════╣
║  Lido stETH      Ethereum   3.2%   -          3.20%      ║
║  Rocket Pool     Ethereum   3.3%   -          3.30%  ⭐  ║
║  Coinbase cbETH  Ethereum   3.1%   -          3.10%      ║
╠══════════════════════════════════════════════════════════╣
║  LP Position Comparison (ETH/USDC)                       ║
╠══════════════════════════════════════════════════════════╣
║  Uniswap V3      Ethereum   12.5%  ~$50/tx    11.0%      ║
║  Uniswap V3      Base       15.2%  ~$0.20/tx  15.2%  ⭐  ║
║  Curve           Ethereum   8.3%   ~$30/tx    7.8%       ║
╚══════════════════════════════════════════════════════════╝

Recommendation: Move USDC lending from Ethereum to Base (Aave V3)
  - Same protocol, same security model
  - Higher APY (4.8% vs 4.5%)
  - Negligible gas costs on Base
  - Estimated annual savings: $450 on $100k deposit
```

### Optimization Strategies

**Gas Fee Arbitrage**:
- For large positions (>$10k), deploy to mainnet (deeper liquidity)
- For smaller positions (<$10k), use L2s (lower gas erosion)
- Monitor gas prices and migrate during low-fee periods

**Protocol Diversification**:
- Don't put all funds in single protocol (smart contract risk)
- Spread across Aave, Compound, Curve, etc.
- Use Zerion to monitor total protocol exposure

**Automated Rebalancing**:
1. Weekly: Compare APYs across chains
2. If delta > 2% for 2+ weeks → Consider migration
3. Calculate break-even point including gas costs
4. Execute migration if profitable

---

## Implementation Best Practices

### 1. Quota Management

**For Free Tier (2 RPS, ~5K requests/day)**:
- Use webhooks instead of polling for real-time data
- Implement client-side caching (5-15 minute TTL)
- Use filters to reduce response sizes
- Batch similar queries

**For Paid Tiers**:
- Builder ($149/mo): 50 RPS → Suitable for small apps
- Pro ($599/mo): 150 RPS → Production applications
- Enterprise: Custom quotas for high-scale use cases

### 2. Data Freshness vs. Quota Trade-offs

| Update Frequency | Use Case | Quota Impact |
|-----------------|----------|--------------|
| **Real-time (webhooks)** | Security monitoring, whale alerts | Minimal (push-based) |
| **5 minutes** | Portfolio dashboards | Moderate (288 req/day per wallet) |
| **Hourly** | Treasury tracking | Low (24 req/day per wallet) |
| **Daily** | Tax reports, analytics | Very low (1 req/day per wallet) |

### 3. Error Handling

- **429 Rate Limit**: Implement exponential backoff (server does this automatically)
- **202 Wallet Indexing**: Retry with 3-5 second delays (server does this automatically)
- **400 Bad Request**: Validate input parameters before calling
- **404 Not Found**: Handle wallets with no activity gracefully

### 4. Data Storage

**Local Caching Strategy**:
- Cache portfolio snapshots (5-15 min TTL)
- Store transaction history (refresh daily)
- Persist PnL calculations (refresh on new transactions)

**Database Schema Recommendations**:
```
wallets
  - address (primary key)
  - last_updated
  - portfolio_value
  - portfolio_change_24h

positions
  - wallet_address (foreign key)
  - fungible_id
  - value_usd
  - quantity
  - chain_id

transactions
  - hash (primary key)
  - wallet_address (foreign key)
  - timestamp
  - operation_type
  - value_usd
  - chain_id
```

### 5. Combining with Other Data Sources

Zerion MCP is powerful but has limitations. Complement with:

| Data Need | Zerion MCP | Alternative Source |
|-----------|------------|-------------------|
| **Wallet balances** | ✅ Excellent | - |
| **DeFi positions** | ✅ Excellent | - |
| **Transaction history** | ✅ Excellent | - |
| **Token holder lists** | ❌ Not available | Etherscan API, Dune Analytics |
| **Historical token prices** | ⚠️ Charts only | CoinGecko, CoinMarketCap |
| **Gas fee predictions** | ⚠️ Current only | ETH Gas Station, Blocknative |
| **On-chain metadata** | ❌ Limited | The Graph, Alchemy |

---

## Security Considerations

### API Key Management
- **Never commit API keys** to version control
- Use environment variables or secret managers
- Rotate keys periodically
- Use separate keys for dev/staging/prod

### Webhook Security
- **HTTPS only** for callback URLs
- Implement signature verification (if Zerion supports)
- IP whitelist Zerion's webhook IPs
- Validate payload structure before processing

### Data Privacy
- **Redact sensitive data** in logs
- Don't expose full wallet addresses in public UIs
- Implement access controls for multi-user dashboards
- GDPR compliance for user wallet tracking

---

## Conclusion

The Zerion MCP Server enables a wide range of cryptocurrency analytics and portfolio management use cases. While it has some limitations (wallet-centric API, no holder discovery), its strengths in multi-chain aggregation, DeFi protocol coverage, and real-time webhooks make it a powerful tool for:

✅ **Portfolio tracking** across 100+ chains
✅ **DeFi position monitoring** for 8,000+ protocols
✅ **Whale watching** with real-time transaction alerts
✅ **Treasury management** for DAOs and protocols
✅ **Trading analytics** and performance tracking
✅ **NFT portfolio** management
✅ **Tax reporting** with FIFO cost basis
✅ **Yield optimization** across chains

For the best results, combine Zerion MCP with complementary data sources (Etherscan for holder lists, CoinGecko for price data, etc.) to build comprehensive crypto analytics applications.

---

## Next Steps

1. **Choose a use case** from this document
2. **Set up Zerion MCP Server** following the README.md
3. **Get an API key** from https://developers.zerion.io/
4. **Start with simple queries** (getWalletPortfolio, listWalletPositions)
5. **Build incrementally** toward your full dashboard
6. **Consider webhooks** for production use (conserves quota)
7. **Monitor quota usage** and upgrade tier as needed

For questions and support:
- GitHub Issues: https://github.com/SAK1337/myzerionmcp/issues
- Zerion API Docs: https://developers.zerion.io/
