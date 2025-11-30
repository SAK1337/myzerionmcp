# Add Webhook Support for Real-Time Transaction Notifications

## Why

The Zerion API provides transaction subscription webhooks (`/v1/tx-subscriptions`) that enable real-time push notifications for wallet activity across EVM and Solana chains. This is **critical** for production applications because:

1. **Rate Limit Conservation**: Without webhooks, applications must continuously poll for transaction updates, rapidly exhausting API quotas (Developer tier: 2 RPS / ~5K requests/day)
2. **Real-Time Capabilities**: Enables building notification systems, alerts, and monitoring dashboards with sub-second latency
3. **Scalability**: Allows efficient monitoring of multiple wallets without quota waste from no-op polling requests
4. **Cost Efficiency**: On paid tiers (Builder: $149/mo), polling wastes quota on redundant requests vs. event-driven updates

The current MCP server implementation **does not expose webhook endpoints** because they are missing from the upstream OpenAPI specification file. This gap blocks 80% of advanced use cases including:
- Wallet transaction alerts for mobile apps
- SocialFi notification systems (like Farcaster integrations)
- Automated trading/bot systems requiring immediate transaction awareness
- Portfolio tracking apps that update "only when new transactions occur"

Additionally, while the OpenAPI spec **already includes** advanced filter parameters (`only_complex`, `filter[chain_ids]`, `filter[trash]`, `filter[operation_types]`), these are not well-documented for MCP users, limiting their usability for DeFi analytics and efficient querying.

## What Changes

### 1. Webhook/Transaction Subscription Endpoints (**CRITICAL**)
Add the following endpoints to the OpenAPI specification and expose them as MCP tools:

- **`POST /v1/tx-subscriptions`** - Create new webhook subscription
- **`GET /v1/tx-subscriptions`** - List all subscriptions
- **`GET /v1/tx-subscriptions/{id}`** - Get subscription details
- **`PATCH /v1/tx-subscriptions/{id}`** - Update subscription (addresses, chains, callback URL)
- **`DELETE /v1/tx-subscriptions/{id}`** - Delete subscription

### 2. Enhanced API Documentation (**HIGH**)
Document existing but underutilized filter parameters:

- **`filter[positions]=only_complex`** - Critical for DeFi-focused applications (isolates staking, LP, lending positions)
- **`filter[chain_ids]`** - Filter by specific blockchains
- **`filter[trash]`** - Hide spam/dust transfers
- **`filter[operation_types]`** - Filter transactions by type (trade, transfer, execute)
- **`filter[position_types]`** - Filter by deposit, loan, staked, reward, etc.

Provide usage examples in README demonstrating:
- How to query DeFi positions only
- Cross-chain filtering
- Spam filtering for clean transaction history
- Operation type filtering for specific analysis

### 3. OpenAPI Specification Enhancement
Update or create extended `openapi_zerion.yaml` with webhook endpoints based on Zerion API documentation.

## Impact

### Affected Specs
- **`webhook-subscriptions`** (NEW) - Transaction subscription management
- **`api-documentation`** (NEW/MODIFIED) - Enhanced filter parameter documentation

### Affected Code
- **`zerion_mcp_server/openapi_zerion.yaml`** - Add webhook endpoint definitions
- **`README.md`** - Add webhook usage guide and filter parameter examples
- **`config.yaml`/`.env.example`** - Document webhook callback URL configuration (if applicable)
- **Tests**: Add integration tests for webhook subscription CRUD operations

### Breaking Changes
**None** - This is purely additive functionality. Existing MCP tools continue to work unchanged.

### Migration
No migration required. New webhook tools will be available alongside existing portfolio/transaction endpoints.

### Dependencies
- Webhook endpoints require HTTP callback URLs (external to MCP server)
- Users must set up separate webhook receiver service or use testing tools like webhook.site
- Webhook signature verification may be needed for production security (future enhancement)

### Risks
- **Architectural consideration**: MCP servers typically run in stdio mode; webhooks require HTTP endpoints. Solution: MCP server manages subscriptions via API calls, but webhook payloads are received by user's separate HTTP service.
- **Documentation complexity**: Need clear examples showing webhook setup flow
- **Spec maintenance**: OpenAPI spec changes must track upstream Zerion API updates
