# API Documentation Enhancements

## ADDED Requirements

### Requirement: Webhook Integration Guide
The README.md SHALL include a comprehensive section explaining how to set up and use webhook subscriptions for real-time transaction monitoring.

#### Scenario: Webhook setup workflow
- **WHEN** a user reads the webhook documentation section
- **THEN** they find step-by-step instructions for:
  1. Setting up a webhook receiver endpoint (external HTTP service)
  2. Creating a subscription using the MCP tool
  3. Testing webhook delivery with webhook.site or similar tool
  4. Parsing webhook payloads in their application
- **AND** each step includes working code examples

#### Scenario: Webhook receiver architecture
- **WHEN** users need to understand the webhook architecture
- **THEN** documentation includes:
  - Diagram showing MCP server → Zerion API → User's HTTP endpoint flow
  - Explanation that MCP server manages subscriptions but does not receive webhooks
  - Guidance on deploying a separate webhook receiver service
  - Example webhook receiver implementations (Python Flask, Express.js, etc.)

#### Scenario: Webhook troubleshooting
- **WHEN** users encounter webhook delivery issues
- **THEN** documentation provides a troubleshooting checklist:
  - Verify callback URL is publicly accessible (HTTPS required)
  - Check subscription is active (not disabled)
  - Verify API key has webhook permissions
  - Test with webhook.site first before production endpoint
  - Review Zerion API documentation for delivery retry policy

---

### Requirement: DeFi Position Filtering Documentation
The README.md SHALL document the `filter[positions]=only_complex` parameter for isolating DeFi protocol positions from simple wallet balances.

#### Scenario: DeFi-only position query
- **WHEN** a user wants to fetch only staking, LP, and lending positions
- **THEN** documentation provides an example showing:
  - How to call `listWalletPositions` with `filter[positions]=only_complex`
  - Explanation of what "complex" positions include (Uniswap LPs, Aave deposits, staking, etc.)
  - Comparison with default behavior (only_simple) and no_filter option
- **AND** example includes actual API response snippets

#### Scenario: Use case explanation
- **WHEN** users need to understand when to use each filter option
- **THEN** documentation explains:
  - `only_simple`: For basic token balance tracking
  - `only_complex`: For DeFi analytics, institutional risk management, yield farming trackers
  - `no_filter`: For complete portfolio view including both types
- **AND** provides real-world use case examples for each

---

### Requirement: Chain Filtering Documentation
The README.md SHALL document the `filter[chain_ids]` parameter for cross-chain and single-chain queries.

#### Scenario: Single-chain query
- **WHEN** a user wants to fetch positions only on Ethereum
- **THEN** documentation shows example using `filter[chain_ids]=ethereum`
- **AND** explains how to find valid chain IDs using the `listChains` tool

#### Scenario: Multi-chain query
- **WHEN** a user wants to track positions across multiple L2s
- **THEN** documentation provides example with `filter[chain_ids]=base,optimism,arbitrum`
- **AND** explains comma-separated syntax for multiple chains

#### Scenario: Cross-endpoint applicability
- **WHEN** users want to know which endpoints support chain filtering
- **THEN** documentation includes a filter applicability matrix showing:
  - `listWalletPositions`: ✅ Supports chain_ids
  - `listWalletTransactions`: ✅ Supports chain_ids
  - `getWalletChart`: ✅ Supports chain_ids
  - `getWalletPortfolio`: ✅ Supports chain_ids
- **AND** notes which endpoints do not support this filter

---

### Requirement: Spam Filtering Documentation
The README.md SHALL document the `filter[trash]` parameter for hiding spam tokens and dust transfers.

#### Scenario: Clean transaction history
- **WHEN** a user wants to hide spam/dust transactions
- **THEN** documentation shows example using `filter[trash]=only_non_trash`
- **AND** explains the three filter options:
  - `only_non_trash`: Exclude spam/dust (recommended for user-facing apps)
  - `only_trash`: Show only spam/dust (for security monitoring)
  - `no_filter`: Show all transactions (default for complete audit)

#### Scenario: Spam detection explanation
- **WHEN** users want to understand how Zerion identifies spam
- **THEN** documentation notes:
  - Zerion uses heuristics to flag spam tokens/transactions
  - Filter is available on transactions, positions, and NFT endpoints
  - Provides link to Zerion documentation for spam detection methodology

---

### Requirement: Transaction Type Filtering Documentation
The README.md SHALL document the `filter[operation_types]` parameter for filtering transactions by operation type.

#### Scenario: Trade-only transactions
- **WHEN** a user wants to analyze only swap/trade activity
- **THEN** documentation shows example using `filter[operation_types]=trade`
- **AND** lists all available operation types:
  - `trade`: Token swaps and DEX trades
  - `transfer`: Simple token transfers
  - `execute`: Smart contract executions
  - Other types as defined by Zerion API

#### Scenario: Multi-type query
- **WHEN** a user wants both trades and transfers but not contract executions
- **THEN** documentation provides example with `filter[operation_types]=trade,transfer`
- **AND** explains comma-separated syntax

---

### Requirement: Position Type Filtering Documentation
The README.md SHALL document the `filter[position_types]` parameter for categorizing DeFi positions.

#### Scenario: Staking positions only
- **WHEN** a user wants to track only staked assets
- **THEN** documentation shows example using `filter[position_types]=staked`
- **AND** lists all position types:
  - `wallet`: Simple balance
  - `deposit`: Lending protocol deposits
  - `loan`: Borrowed assets
  - `staked`: Staked tokens
  - `reward`: Claimable rewards
  - `locked`: Vested/locked tokens
  - `margin`: Margin positions
  - `airdrop`: Airdrop eligibility

#### Scenario: Multi-type position tracking
- **WHEN** a user wants to track both staked assets and claimable rewards
- **THEN** documentation provides example with `filter[position_types]=staked,reward`

---

### Requirement: Query Optimization Guide
The README.md SHALL include a section on using filters to optimize API quota usage and improve response times.

#### Scenario: Rate limit conservation
- **WHEN** users need to minimize API calls on limited quota tiers
- **THEN** documentation explains:
  - Use specific chain filters instead of fetching all chains
  - Use `only_non_trash` to reduce response size and parsing time
  - Use operation_types filters to avoid processing irrelevant transactions
  - Combine filters to get precisely what you need in one call
- **AND** provides before/after examples showing quota savings

#### Scenario: Performance optimization
- **WHEN** users experience slow response times
- **THEN** documentation recommends:
  - Filter at API level rather than client-side post-processing
  - Request smaller page sizes for large wallets
  - Use only_complex when DeFi data is all that's needed
- **AND** explains the performance impact of each filter

---

### Requirement: Filter Applicability Matrix
The README.md SHALL include a table showing which filters are available on which endpoints to avoid confusion and trial-and-error testing.

#### Scenario: Quick filter reference
- **WHEN** a user wants to know if `filter[trash]` works on a specific endpoint
- **THEN** they consult the filter matrix table showing:

| Endpoint | chain_ids | trash | operation_types | position_types | positions | fungible_ids |
|----------|-----------|-------|-----------------|----------------|-----------|--------------|
| listWalletPositions | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| listWalletTransactions | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ |
| getWalletChart | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ |
| getWalletPortfolio | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ |

- **AND** each checkmark links to a usage example for that filter+endpoint combination

---

### Requirement: Configuration Examples for Advanced Usage
The README.md SHALL include example configurations showing how to structure complex queries with multiple filters.

#### Scenario: Complex query example
- **WHEN** a user wants to build a DeFi-only, spam-free, Ethereum-only position tracker
- **THEN** documentation provides a complete example showing:
```
Tool: listWalletPositions
Parameters:
  address: "0x42b9dF65B219B3dD36FF330A4dD8f327A6Ada990"
  filter[positions]: "only_complex"
  filter[chain_ids]: "ethereum"
  filter[trash]: "only_non_trash"
  currency: "usd"
  sort: "value"
```
- **AND** shows the expected response structure

#### Scenario: Transaction analysis query
- **WHEN** a user wants to analyze only Base and Optimism trades excluding spam
- **THEN** documentation provides example:
```
Tool: listWalletTransactions
Parameters:
  address: "0x..."
  filter[chain_ids]: "base,optimism"
  filter[operation_types]: "trade"
  filter[trash]: "only_non_trash"
  page[size]: 100
```

---

### Requirement: Error Message Clarity
Documentation SHALL explain common error messages related to filters and how to resolve them.

#### Scenario: Invalid filter value
- **WHEN** user provides an invalid filter value (e.g., `filter[positions]=invalid`)
- **THEN** documentation explains:
  - API returns 400 Bad Request
  - Error message indicates which parameter is invalid
  - Lists valid options for that filter
- **AND** provides troubleshooting guidance

#### Scenario: Filter combination not supported
- **WHEN** user tries to combine filters in an unsupported way
- **THEN** documentation explains:
  - Which filter combinations are valid
  - Why certain combinations don't make sense (e.g., operation_types on position endpoints)
- **AND** suggests alternative query strategies
