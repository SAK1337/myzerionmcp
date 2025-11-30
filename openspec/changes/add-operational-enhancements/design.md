# Operational Enhancements Design Document

## Context

The Zerion MCP Server provides access to portfolio, transaction, and NFT data through auto-generated MCP tools. However, three operational gaps create poor user experience in production:

1. **Pagination**: Active wallets with thousands of transactions cannot retrieve complete histories
2. **Rate Limiting**: API quota exhaustion (429) has no retry logic or visibility
3. **202 Accepted**: Newly indexed wallets require retry logic that doesn't exist

### Stakeholders
- **MCP Server Users**: Developers building applications needing reliable data access
- **Production Deployments**: Applications on paid tiers ($149-$599/mo) requiring 99% uptime
- **API Quota Management**: Teams needing efficient quota usage and monitoring

### Constraints
- Must maintain backward compatibility (no breaking changes)
- Retry logic should be transparent to users
- Pagination helpers should be optional (some users want manual control)
- Configuration must be simple and well-documented

---

## Goals / Non-Goals

### Goals
✅ Enable retrieval of complete result sets (pagination)
✅ Automatic retry on rate limit exhaustion (429)
✅ Automatic retry on wallet indexing (202)
✅ Surface quota status to users
✅ Enhance error messages with actionable guidance
✅ Maintain backward compatibility

### Non-Goals
❌ Build custom rate limiting (use Zerion's quotas)
❌ Implement client-side caching (out of scope)
❌ Create webhook-based quota notifications
❌ Modify OpenAPI spec (use existing pagination params)

---

## Decisions

### Decision 1: Pagination Strategy

**Choice**: Expose existing pagination parameters + optional auto-pagination helper.

**Rationale**:
- OpenAPI spec already includes `page[size]` and `page[after]` parameters
- Some users want manual control (fetch one page at a time)
- Others want convenience (fetch all pages automatically)
- Provide both: expose params + helper function

**Implementation**:
```python
# Manual pagination (existing - just document it)
response = listWalletTransactions(
    address="0x...",
    page_size=100
)
next_cursor = response["links"]["next"]  # Use for next request

# Auto-pagination helper (NEW)
from zerion_mcp_server.pagination import fetch_all_pages

all_transactions = await fetch_all_pages(
    endpoint="listWalletTransactions",
    address="0x...",
    max_pages=50  # Safety limit
)
```

**Alternatives Considered**:
1. ❌ **Auto-paginate by default**: Could cause unexpected quota usage
2. ❌ **No helper function**: Too manual for common use case
3. ✅ **Expose + helper**: Best of both worlds

---

### Decision 2: Rate Limit Retry Strategy

**Choice**: Implement exponential backoff with jitter using `tenacity` library.

**Rationale**:
- Zerion returns `429 Too Many Requests` when quota exceeded
- `Retry-After` header provides reset time
- Exponential backoff prevents thundering herd
- `tenacity` library provides battle-tested retry logic

**Implementation**:
```python
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

@retry(
    retry=retry_if_exception_type(RateLimitError),
    wait=wait_exponential(multiplier=1, min=1, max=60),
    stop=stop_after_attempt(5),
    reraise=True
)
async def call_api_with_retry(endpoint, **params):
    response = await client.request(endpoint, **params)
    if response.status_code == 429:
        retry_after = int(response.headers.get("Retry-After", 30))
        raise RateLimitError(f"Rate limit exceeded. Retry after {retry_after}s")
    return response
```

**Configuration**:
```yaml
retry_policy:
  max_attempts: 5
  base_delay: 1  # seconds
  max_delay: 60  # seconds
  exponential_base: 2
```

**Alternatives Considered**:
1. ❌ **No retry**: Poor UX, users see failures
2. ❌ **Fixed delay**: Doesn't scale with load
3. ✅ **Exponential backoff with jitter**: Industry standard

---

### Decision 3: 202 Accepted Handling

**Choice**: Automatic retry with fixed delay for newly indexed wallets.

**Rationale**:
- `202 Accepted` indicates wallet is being indexed (first request)
- Zerion documentation recommends retry after 2-5 seconds
- This is a transient state, not rate limiting
- Should be transparent to users

**Implementation**:
```python
async def handle_202_accepted(endpoint, **params):
    response = await client.request(endpoint, **params)

    if response.status_code == 202:
        logger.info(f"Wallet being indexed, retrying in {retry_delay}s")
        for attempt in range(max_retries):
            await asyncio.sleep(retry_delay)
            response = await client.request(endpoint, **params)
            if response.status_code == 200:
                return response

        raise WalletIndexingError("Wallet indexing timeout")

    return response
```

**Configuration**:
```yaml
wallet_indexing:
  retry_delay: 3  # seconds
  max_retries: 3
```

**Alternatives Considered**:
1. ❌ **No retry**: Users see failures for new wallets
2. ❌ **Exponential backoff**: Overkill for predictable delay
3. ✅ **Fixed delay**: Simple, matches Zerion's guidance

---

## Risks / Trade-offs

### Risk 1: Pagination Quota Consumption

**Description**: Auto-pagination could consume quota rapidly if user requests many pages.

**Mitigation**:
- Default `max_pages` limit (e.g., 50 pages)
- Log warnings at 10, 25, 50 page thresholds
- Document quota impact in README
- Provide manual pagination as alternative

**Severity**: Medium (mitigated with limits)

---

### Risk 2: Retry Logic Delays

**Description**: Automatic retries add latency to responses.

**Mitigation**:
- Exponential backoff prevents excessive delays
- Log retry attempts for visibility
- Make retry configurable (users can disable)
- Document expected latency in README

**Severity**: Low (acceptable trade-off for reliability)

---

### Risk 3: 202 Retry Timeout

**Description**: Wallet indexing may take longer than configured retry period.

**Mitigation**:
- Default 3 retries × 3 seconds = 9 seconds total
- Allow configuration of retry count and delay
- Clear error message if indexing times out
- Suggest user retry manually after 30 seconds

**Severity**: Low (rare edge case)

---

## Migration Plan

### Phase 1: Core Implementation
1. Add `tenacity` dependency to pyproject.toml
2. Implement retry decorators and error classes
3. Add pagination helper function
4. Update configuration schema

### Phase 2: Integration
1. Apply retry logic to API client
2. Integrate 202 handling into request flow
3. Add pagination helpers to __init__.py exports
4. Test with real API

### Phase 3: Documentation
1. Add pagination guide to README
2. Add rate limiting guide to README
3. Update troubleshooting section
4. Add configuration examples

### Phase 4: Testing & Validation
1. Unit tests for all retry logic
2. Integration tests with mocked 429/202 responses
3. Manual testing with real quota exhaustion
4. Performance testing for pagination

### Rollback Plan
If issues arise:
1. Retry logic is decorator-based (easy to disable via config)
2. Pagination helpers are opt-in (don't affect existing code)
3. Existing error handling unchanged (fallback behavior)

---

## Success Metrics

- ✅ Users can retrieve 5000+ transactions without manual pagination
- ✅ 429 responses automatically retry with backoff (no user intervention)
- ✅ 202 responses automatically retry until data ready
- ✅ Error messages include quota status and next steps
- ✅ Test coverage >90% for retry and pagination logic
- ✅ Zero breaking changes to existing tools

---

## Open Questions

### Q1: Should pagination helpers be async generators?
**Status**: Design decision needed
**Options**:
- Generator: Memory efficient, streams results
- List: Simpler API, all results at once
**Action**: Start with list, add generator if requested

### Q2: Should we cache rate limit status?
**Status**: Out of scope for this proposal
**Impact**: Could reduce redundant 429 responses
**Action**: Document as future enhancement

### Q3: What's the ideal max_pages default?
**Status**: Set to 50 based on quota analysis
**Reasoning**: 50 pages × 100 items = 5000 results (covers 99% of wallets)
**Action**: Make configurable, document trade-offs

---

## References

- [Zerion API Documentation - Pagination](https://developers.zerion.io/reference)
- [Tenacity Library Documentation](https://tenacity.readthedocs.io/)
- Gap Analysis Document (GapAnalysis.md sections 2.4-2.6)
