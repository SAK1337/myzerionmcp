# Add Operational Enhancements for Production Reliability

## Why

The Zerion MCP Server currently lacks critical operational features needed for production deployments, specifically around handling large result sets, rate limiting, and special API response codes. These gaps create poor user experience and potential reliability issues:

1. **Pagination Limitations**: Users cannot retrieve complete transaction histories for active wallets. A wallet with 5,000 transactions may only return the first 100 results with no way to fetch subsequent pages.

2. **Rate Limit Handling**: When API quotas are exhausted (429 responses), there's no intelligent retry logic, exponential backoff, or visibility into quota status. This leads to failed requests and poor error messages.

3. **202 Accepted Responses**: Newly indexed wallets return `202 Accepted` status requiring retry logic. Without handling this, users see failures for valid requests.

These issues are blockers for production use, especially on constrained API tiers (Developer: 2 RPS / ~5K daily, Builder: $149/mo).

## What Changes

### 1. Pagination Handling (**HIGH PRIORITY**)
- Expose `page[size]` and `page[after]` parameters in tool schemas (if not already exposed)
- Document pagination workflow in README with examples
- Add pagination helper utilities (optional auto-fetch)
- Return `links.next` URLs in responses for manual continuation

### 2. Rate Limit & Error Handling (**MEDIUM PRIORITY**)
- Detect `429 Too Many Requests` responses
- Parse `Retry-After` header and implement exponential backoff with jitter
- Surface quota status to users (requests remaining, reset time)
- Log rate limit events for monitoring
- Enhance error messages with actionable guidance

### 3. 202 Accepted Response Handling (**MEDIUM PRIORITY**)
- Detect `202 Accepted` for newly indexed wallets
- Implement automatic retry with configurable delay (2-5 seconds)
- Inform users when wallet is being indexed
- Add configuration for max retries and retry delay

## Impact

### Affected Specs
- **`pagination-handling`** (NEW) - Cursor-based pagination for large result sets
- **`rate-limit-handling`** (NEW) - Intelligent quota management and retry logic
- **`response-handling`** (NEW) - 202 Accepted status handling

### Affected Code
- **`zerion_mcp_server/__init__.py`** - Add pagination helpers, retry logic
- **`zerion_mcp_server/errors.py`** - Add RateLimitError, RetryableError
- **`zerion_mcp_server/config.py`** - Add retry/pagination config options
- **`README.md`** - Document pagination, rate limits, error handling
- **Tests**: Add unit tests for pagination, rate limiting, 202 handling

### Breaking Changes
**None** - Purely additive enhancements. Existing behavior unchanged.

### Migration
No migration required. New features are opt-in via configuration or automatic (retry logic).

### Dependencies
- Requires `tenacity` library for retry logic (add to pyproject.toml dependencies)
- Pagination helpers use existing httpx client
