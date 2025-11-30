# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2025-11-30

### Added - Webhook Support for Real-Time Notifications

#### Critical New Features
- **Webhook Subscription Management**: 5 new MCP tools for transaction subscriptions
  - `createTxSubscription` - Create webhook for wallet activity monitoring
  - `listTxSubscriptions` - List all active subscriptions
  - `getTxSubscription` - Get subscription details by ID
  - `updateTxSubscription` - Update addresses, callback URL, or chain filters
  - `deleteTxSubscription` - Delete subscription permanently

- **Real-Time Transaction Monitoring**: Enable sub-second notifications when monitored wallets transact on EVM or Solana chains
- **Rate Limit Optimization**: Webhooks eliminate inefficient polling, conserving API quotas (critical for free tier: ~5K requests/day)

#### Documentation Enhancements

- **Comprehensive Webhook Guide** (README):
  - Architecture diagram showing MCP server → Zerion API → User's HTTP receiver flow
  - 3 webhook receiver implementation examples (webhook.site, Python Flask, Node.js Express)
  - Webhook payload structure documentation with real examples
  - Security best practices (HTTPS requirement, signature verification notes)
  - Troubleshooting guide for common webhook delivery issues

- **Advanced Filtering Guide** (README):
  - **DeFi Position Filtering (`only_complex`)**: Isolate staking, LP, and lending positions from simple balances
  - **Chain Filtering (`filter[chain_ids]`)**: Query specific blockchains (Ethereum, Base, Optimism, etc.)
  - **Spam Filtering (`filter[trash]`)**: Hide spam/dust transfers for clean transaction history
  - **Operation Type Filtering (`filter[operation_types]`)**: Filter by trade, transfer, execute
  - **Position Type Filtering (`filter[position_types]`)**: Categorize by staked, deposit, loan, reward
  - **Filter Applicability Matrix**: Table showing which filters work on which endpoints
  - **Query Optimization Best Practices**: Examples showing 20x reduction in response size
  - **Common Filter Combinations**: Use-case specific query patterns

#### Testing
- **14 New Integration Tests** (`tests/test_webhooks.py`):
  - Webhook subscription creation (Ethereum & Solana)
  - Subscription listing and pagination
  - Subscription retrieval by ID
  - Subscription updates (addresses, callback URL, chain filters)
  - Subscription deletion
  - Webhook payload structure validation
  - Rate limiting (429 responses)
  - Error handling (400, 404 responses)
  - All tests passing with 100% success rate

#### Configuration
- Added `WEBHOOK_CALLBACK_URL` to `.env.example` with usage notes
- Added webhook configuration section to `config.example.yaml`
- Documented that webhook receiver must be deployed separately (MCP server manages subscriptions only)

### Technical Details

#### OpenAPI Specification
- Extended `openapi_zerion.yaml` with 5 new webhook endpoints (lines 1334-1685)
- Comprehensive request/response schemas with examples
- Proper error response definitions (400, 401, 404, 429)
- Operation IDs matching MCP tool naming conventions

#### Architecture
- **Separation of Concerns**: MCP server (stdio mode) manages subscriptions via API; user's HTTP service receives webhook payloads
- **No Breaking Changes**: Purely additive functionality; all existing tools continue to work
- **FastMCP Integration**: Webhook tools auto-generated from OpenAPI spec

### Use Cases Enabled

- **Wallet Transaction Alerts**: Mobile apps, browser extensions
- **SocialFi Notifications**: Farcaster, Lens Protocol integrations
- **Trading Bots**: Immediate transaction awareness for automated strategies
- **Portfolio Trackers**: Update only when transactions occur (quota efficient)
- **DeFi Analytics**: Institutional-grade risk dashboards using `only_complex` filter
- **L2 Analytics**: Cross-chain trading analysis with chain filters
- **Tax Reporting**: Clean transaction history with spam filtering

### Migration Notes

- **No migration required** - all changes are backward compatible
- Existing MCP tools (portfolio, transactions, NFTs, etc.) unchanged
- New webhook tools available immediately after update
- Filter parameters already existed in API; now documented for visibility

### Known Limitations

- Webhook receiver must be deployed separately (external HTTP service)
- Developer tier: Limited subscriptions (1-5), shorter validity
- Callback URLs must be HTTPS (HTTP not supported)
- Webhook delivery order not guaranteed (matches blockchain timing)
- Contact api@zerion.io for enterprise webhook quotas

## [Unreleased]

### Added
- **Configuration System**: YAML-based configuration with environment variable overrides
  - ConfigManager class for flexible configuration loading
  - Support for config.yaml files with ${VAR} substitution
  - Environment variables: ZERION_API_KEY, ZERION_BASE_URL, LOG_LEVEL, etc.
  - Example configuration file (config.example.yaml)
  
- **Logging Infrastructure**: Structured logging with multiple formats
  - JSON and text log formats
  - Configurable log levels (DEBUG, INFO, WARN, ERROR)
  - Automatic sensitive data redaction (API keys, Bearer tokens)
  - Request/response logging with timing metrics
  - Performance logging for operations
  
- **Error Handling**: Comprehensive custom exception hierarchy
  - ConfigError for configuration issues
  - NetworkError for connectivity problems
  - APIError for Zerion API failures with status code handling
  - ValidationError for data validation issues
  - Detailed error contexts and troubleshooting hints
  
- **Testing Infrastructure**: Full test suite with pytest
  - Unit tests for configuration (test_config.py)
  - Unit tests for error handling (test_errors.py)
  - Integration tests for server flow (test_integration.py)
  - Test fixtures and mocks (conftest.py)
  - Coverage reporting configuration
  - Development dependencies in pyproject.toml
  
- **Documentation**: Comprehensive project documentation
  - Detailed README with installation, configuration, and usage
  - Troubleshooting guide with common issues and solutions
  - Architecture diagram
  - Contributing guidelines
  - This CHANGELOG

### Changed
- **Server Initialization**: Enhanced error handling during startup
  - Better error messages for missing API keys
  - Detailed logging of initialization steps
  - Graceful handling of OpenAPI spec loading failures
  
- **HTTP Client**: Improved configuration
  - Configurable timeouts (30 seconds default)
  - Better exception handling for network errors
  - Status code validation with raise_for_status()

### Fixed
- None (initial production-ready release)

## [0.1.0] - Initial Release

### Added
- Basic MCP server functionality
- FastMCP integration with OpenAPI spec
- Zerion API proxy via MCP protocol
- httpx async HTTP client
- Basic package structure

[Unreleased]: https://github.com/SAK1337/myzerionmcp/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/SAK1337/myzerionmcp/releases/tag/v0.1.0
