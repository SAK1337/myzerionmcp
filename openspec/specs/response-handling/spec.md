# response-handling Specification

## Purpose
TBD - created by archiving change add-operational-enhancements. Update Purpose after archive.
## Requirements
### Requirement: 202 Accepted Detection
The MCP server SHALL detect `202 Accepted` responses from the Zerion API indicating wallet indexing is in progress and handle them appropriately.

#### Scenario: Detect 202 Accepted response
- **WHEN** Zerion API returns `202 Accepted` status
- **THEN** the MCP server recognizes this as wallet indexing in progress
- **AND** prepares for automatic retry
- **AND** logs indexing event

#### Scenario: First request to new wallet
- **WHEN** user requests portfolio for newly created wallet address
- **THEN** Zerion returns `202 Accepted`
- **AND** MCP server handles retry automatically
- **AND** user receives data once indexing completes

---

### Requirement: Automatic 202 Retry Logic
The MCP server SHALL automatically retry requests that receive `202 Accepted` responses with a fixed delay until data is ready or max retries are exhausted.

#### Scenario: Successful retry after 202
- **WHEN** first request returns `202 Accepted`
- **THEN** the MCP server waits configured delay (default 3 seconds)
- **AND** retries the request
- **AND** returns `200 OK` response with data
- **AND** logs successful wallet indexing

#### Scenario: Multiple 202 retries
- **WHEN** wallet indexing takes longer than one retry cycle
- **THEN** the MCP server retries up to max_retries times (default 3)
- **AND** waits fixed delay between each retry
- **AND** logs retry attempt number

#### Scenario: 202 timeout
- **WHEN** wallet indexing not complete after max retries
- **THEN** the MCP server raises `WalletIndexingError`
- **AND** error message explains wallet is still indexing
- **AND** suggests user retry manually after 30 seconds

#### Scenario: Immediate success
- **WHEN** first request returns `200 OK` (wallet already indexed)
- **THEN** no retry logic triggers
- **AND** response returned immediately

---

### Requirement: 202 Retry Configuration
The MCP server SHALL allow configuration of 202 retry behavior including delay duration and maximum retry attempts.

#### Scenario: Configure retry delay
- **WHEN** config.yaml sets `wallet_indexing.retry_delay: 5`
- **THEN** the MCP server waits 5 seconds between 202 retries
- **AND** users can adjust based on observed indexing times

#### Scenario: Configure max retries
- **WHEN** config.yaml sets `wallet_indexing.max_retries: 5`
- **THEN** the MCP server retries up to 5 times
- **AND** total wait time is 5 × 5 = 25 seconds max

#### Scenario: Disable 202 auto-retry
- **WHEN** config.yaml sets `wallet_indexing.auto_retry: false`
- **THEN** 202 responses immediately raise error to user
- **AND** error message explains wallet is indexing

---

### Requirement: Wallet Indexing Status Logging
The MCP server SHALL log wallet indexing events for monitoring and debugging purposes.

#### Scenario: Log 202 detection
- **WHEN** 202 Accepted response received
- **THEN** the MCP server logs:
  - Wallet address being indexed
  - Timestamp of initial request
  - Retry delay configuration
- **AND** log level is INFO

#### Scenario: Log retry attempts
- **WHEN** retrying after 202
- **THEN** the MCP server logs:
  - Retry attempt number (e.g., "Retry 2/3")
  - Elapsed time since first request
- **AND** log level is INFO

#### Scenario: Log successful indexing
- **WHEN** wallet indexing completes and data returned
- **THEN** the MCP server logs:
  - Total indexing time
  - Number of retries required
  - Wallet address
- **AND** log level is INFO

#### Scenario: Log indexing timeout
- **WHEN** max retries exhausted
- **THEN** the MCP server logs:
  - Wallet address
  - Total attempts
  - Total wait time
  - "Indexing timeout" message
- **AND** log level is WARNING

---

### Requirement: Enhanced Error Messages for Indexing
The MCP server SHALL provide clear error messages when wallet indexing times out, with guidance for users.

#### Scenario: Indexing timeout error message
- **WHEN** wallet indexing times out after max retries
- **THEN** error message includes:
  - "Wallet is still being indexed by Zerion"
  - "Tried X times over Y seconds"
  - "Please retry in 30-60 seconds"
  - Wallet address that was requested

#### Scenario: Error message for immediate 202
- **WHEN** auto-retry is disabled and 202 received
- **THEN** error message includes:
  - "Wallet indexing in progress"
  - "This is a new wallet address for Zerion"
  - "Enable auto_retry or wait and retry manually"

---

### Requirement: 202 Handling Documentation
The README SHALL document 202 Accepted behavior, automatic retry logic, and configuration options.

#### Scenario: 202 behavior explanation
- **WHEN** user reads 202 handling documentation
- **THEN** they find explanation of:
  - What 202 Accepted means (wallet indexing)
  - When it occurs (first request to new wallet)
  - How automatic retry works
  - Expected indexing time (2-10 seconds typically)

#### Scenario: Configuration documentation
- **WHEN** user reads 202 handling documentation
- **THEN** they find configuration options:
  - `retry_delay`: Wait time between retries
  - `max_retries`: Maximum retry attempts
  - `auto_retry`: Enable/disable automatic retry

#### Scenario: Troubleshooting guidance
- **WHEN** user reads 202 handling documentation
- **THEN** they find troubleshooting steps:
  - "Indexing timeout" → wait 30s and retry
  - "New wallet address" → expected behavior
  - "Configure longer delay" → for slow indexing

