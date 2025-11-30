# Rate Limit Handling Capability

## ADDED Requirements

### Requirement: Rate Limit Detection
The MCP server SHALL detect `429 Too Many Requests` responses from the Zerion API and raise a specific `RateLimitError` exception with quota status information.

#### Scenario: Detect 429 response
- **WHEN** Zerion API returns `429 Too Many Requests`
- **THEN** the MCP server raises `RateLimitError` exception
- **AND** exception includes `Retry-After` header value if present
- **AND** exception message explains quota exhaustion

#### Scenario: Parse Retry-After header
- **WHEN** 429 response includes `Retry-After: 30` header
- **THEN** the error message includes "Retry after 30 seconds"
- **AND** automatic retry logic respects this delay

#### Scenario: No Retry-After header
- **WHEN** 429 response lacks `Retry-After` header
- **THEN** the MCP server uses default backoff strategy
- **AND** logs warning about missing header

---

### Requirement: Automatic Retry with Exponential Backoff
The MCP server SHALL automatically retry requests that fail with `429 Too Many Requests` using exponential backoff with jitter.

#### Scenario: First retry after rate limit
- **WHEN** request fails with 429 response
- **THEN** the MCP server waits 1 second (base delay)
- **AND** retries the request automatically
- **AND** logs retry attempt with delay duration

#### Scenario: Exponential backoff on repeated failures
- **WHEN** request fails with 429 three times consecutively
- **THEN** retry delays increase exponentially: 1s, 2s, 4s
- **AND** jitter prevents thundering herd effect
- **AND** max delay capped at configured limit (default 60s)

#### Scenario: Successful retry
- **WHEN** retry succeeds after 429
- **THEN** the MCP server returns successful response
- **AND** logs successful retry for monitoring
- **AND** no error visible to end user

#### Scenario: Max retries exhausted
- **WHEN** request fails with 429 after max retry attempts (default 5)
- **THEN** the MCP server raises `RateLimitError` to user
- **AND** error message includes total attempts and next reset time
- **AND** error message suggests upgrading tier or waiting

---

### Requirement: Retry Configuration
The MCP server SHALL allow configuration of retry behavior including max attempts, delays, and backoff strategy.

#### Scenario: Configure max retry attempts
- **WHEN** config.yaml sets `retry_policy.max_attempts: 3`
- **THEN** the MCP server stops retrying after 3 failed attempts
- **AND** raises error to user on final failure

#### Scenario: Configure backoff delays
- **WHEN** config.yaml sets `retry_policy.base_delay: 2` and `retry_policy.max_delay: 120`
- **THEN** first retry waits 2 seconds
- **AND** delays cap at 120 seconds for long waits

#### Scenario: Disable automatic retry
- **WHEN** config.yaml sets `retry_policy.enabled: false`
- **THEN** 429 responses immediately raise error to user
- **AND** no automatic retry occurs

---

### Requirement: Rate Limit Status Logging
The MCP server SHALL log rate limit events including quota status, retry attempts, and reset times for monitoring and debugging.

#### Scenario: Log rate limit event
- **WHEN** 429 response received
- **THEN** the MCP server logs:
  - Timestamp of rate limit hit
  - Endpoint that failed
  - Retry-After value
  - Current retry attempt number
- **AND** log level is WARNING

#### Scenario: Log successful retry
- **WHEN** retry succeeds after rate limit
- **THEN** the MCP server logs:
  - Successful retry after N attempts
  - Total delay duration
  - Endpoint that succeeded
- **AND** log level is INFO

---

### Requirement: Enhanced Error Messages
The MCP server SHALL provide actionable error messages when rate limits are exhausted, including quota status and remediation guidance.

#### Scenario: Rate limit error message includes guidance
- **WHEN** max retries exhausted
- **THEN** error message includes:
  - "Rate limit exceeded after 5 retry attempts"
  - "Retry after XX seconds" (from header)
  - "Consider upgrading tier or reducing request frequency"
  - Link to Zerion pricing page

#### Scenario: Tier-specific guidance
- **WHEN** rate limit error on Developer tier (2 RPS)
- **THEN** error message suggests:
  - Using webhooks instead of polling
  - Upgrading to Builder tier ($149/mo, 50 RPS)
  - Implementing client-side caching

---

### Requirement: Rate Limit Documentation
The README SHALL include comprehensive rate limiting documentation with tier comparison, retry behavior, and best practices.

#### Scenario: Tier comparison table
- **WHEN** user reads rate limiting documentation
- **THEN** they find table showing:
  - Developer tier: 2 RPS, ~5K daily
  - Builder tier: 50 RPS, ~500K daily
  - Pro tier: 150 RPS, ~1.5M daily
  - Enterprise tier: Custom limits

#### Scenario: Automatic retry documentation
- **WHEN** user reads rate limiting documentation
- **THEN** they find explanation of:
  - Exponential backoff strategy
  - Max retry attempts (default 5)
  - How to disable retries
  - Configuration options

#### Scenario: Best practices for quota management
- **WHEN** user reads rate limiting documentation
- **THEN** they find guidance on:
  - Using webhooks to avoid polling
  - Implementing client-side caching
  - Optimizing with filters (reduce response size)
  - Monitoring quota usage
