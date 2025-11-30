# Webhook Subscriptions Capability

## ADDED Requirements

### Requirement: Transaction Subscription Creation
The MCP server SHALL expose a tool to create transaction subscription webhooks via the Zerion API `POST /v1/tx-subscriptions` endpoint, enabling real-time push notifications for wallet activity.

#### Scenario: Create EVM subscription
- **WHEN** user calls the create subscription tool with:
  - `addresses`: ["0x42b9dF65B219B3dD36FF330A4dD8f327A6Ada990"]
  - `callback_url`: "https://webhook.site/test-endpoint"
  - `chain_ids`: ["ethereum", "base"]
- **THEN** the API creates a new subscription and returns:
  - Subscription ID
  - Subscription attributes (addresses, callback_url, timestamp)
  - HTTP 201 Created status

#### Scenario: Create Solana subscription
- **WHEN** user calls the create subscription tool with:
  - `addresses`: ["8BH9pjtgyZDC4iAQH5ZiYDZ1MDWC98xki2V8NzqqKW3K"]
  - `callback_url`: "https://webhook.site/test-endpoint"
  - `chain_ids`: ["solana"]
- **THEN** the API creates a Solana-specific subscription
- **AND** returns subscription ID and configuration

#### Scenario: Multi-wallet subscription
- **WHEN** user provides multiple wallet addresses in a single subscription
- **THEN** the API creates one subscription monitoring all specified addresses
- **AND** sends webhook notifications for transactions from any monitored wallet

#### Scenario: Invalid callback URL
- **WHEN** user provides an invalid or non-HTTPS callback URL
- **THEN** the API returns 400 Bad Request
- **AND** the error message explains the callback URL requirement

---

### Requirement: Subscription Listing
The MCP server SHALL expose a tool to list all active transaction subscriptions via the Zerion API `GET /v1/tx-subscriptions` endpoint.

#### Scenario: List subscriptions
- **WHEN** user calls the list subscriptions tool
- **THEN** the API returns an array of all subscriptions associated with the API key
- **AND** each subscription includes:
  - Subscription ID
  - Monitored addresses
  - Callback URL
  - Chain IDs
  - Creation timestamp
  - Enabled/disabled status

#### Scenario: No subscriptions exist
- **WHEN** user has no active subscriptions
- **THEN** the API returns an empty array
- **AND** HTTP 200 OK status

---

### Requirement: Subscription Retrieval
The MCP server SHALL expose a tool to retrieve a specific subscription by ID via the Zerion API `GET /v1/tx-subscriptions/{id}` endpoint.

#### Scenario: Get subscription by ID
- **WHEN** user calls the get subscription tool with a valid subscription ID
- **THEN** the API returns the full subscription details including:
  - All monitored addresses
  - Callback URL
  - Chain filters
  - Metadata (created timestamp, status)

#### Scenario: Subscription not found
- **WHEN** user requests a subscription ID that does not exist
- **THEN** the API returns 404 Not Found
- **AND** error message indicates the subscription ID is invalid

---

### Requirement: Subscription Update
The MCP server SHALL expose a tool to update an existing subscription via the Zerion API `PATCH /v1/tx-subscriptions/{id}` endpoint, allowing modification of monitored addresses, callback URL, and chain filters.

#### Scenario: Add addresses to subscription
- **WHEN** user calls the update tool to add new wallet addresses to an existing subscription
- **THEN** the API updates the subscription to monitor the additional addresses
- **AND** returns the updated subscription object

#### Scenario: Change callback URL
- **WHEN** user updates the callback_url parameter
- **THEN** future webhook notifications are sent to the new URL
- **AND** the change takes effect immediately

#### Scenario: Update chain filters
- **WHEN** user modifies the chain_ids array (e.g., adding "optimism" to existing ["ethereum"])
- **THEN** the subscription monitors transactions on all specified chains
- **AND** historical chains remain monitored unless explicitly removed

---

### Requirement: Subscription Deletion
The MCP server SHALL expose a tool to delete a subscription via the Zerion API `DELETE /v1/tx-subscriptions/{id}` endpoint, permanently removing the webhook configuration.

#### Scenario: Delete subscription
- **WHEN** user calls the delete subscription tool with a valid subscription ID
- **THEN** the API removes the subscription
- **AND** no further webhook notifications are sent
- **AND** returns HTTP 204 No Content

#### Scenario: Delete already deleted subscription
- **WHEN** user attempts to delete a subscription that was already deleted
- **THEN** the API returns 404 Not Found
- **AND** error message indicates the subscription does not exist

---

### Requirement: Webhook Payload Structure
The MCP server documentation SHALL describe the expected webhook payload format that users will receive at their callback URL when subscribed transactions occur.

#### Scenario: Webhook payload documentation
- **WHEN** a user sets up a webhook subscription
- **THEN** the README documentation provides:
  - Complete JSON schema of webhook payloads
  - Example payload for EVM transaction
  - Example payload for Solana transaction
  - Description of all payload fields (hash, mined_at, transfers, fee, etc.)

#### Scenario: Webhook signature verification guidance
- **WHEN** users need to secure their webhook endpoints
- **THEN** documentation explains:
  - How Zerion signs webhook requests (if applicable)
  - How to verify webhook authenticity
  - Security best practices for callback endpoints

---

### Requirement: Tool Parameter Validation
The MCP server SHALL validate tool parameters before making API requests to provide clear error messages for invalid inputs.

#### Scenario: Missing required parameter
- **WHEN** user calls create subscription without providing `callback_url`
- **THEN** the tool returns a validation error
- **AND** error message specifies which required parameter is missing

#### Scenario: Invalid chain ID
- **WHEN** user provides an unsupported chain ID (e.g., "invalid-chain")
- **THEN** the API returns 400 Bad Request
- **AND** error suggests valid chain IDs or references the chains endpoint

---

### Requirement: Rate Limit Awareness
Webhook subscription operations SHALL respect Zerion API rate limits and provide meaningful error handling when limits are exceeded.

#### Scenario: Rate limit on subscription creation
- **WHEN** user exceeds the rate limit for subscription operations
- **THEN** the API returns 429 Too Many Requests
- **AND** error message includes retry-after information (if provided by Zerion)
- **AND** documentation advises users on rate limit handling

---

### Requirement: OpenAPI Specification Completeness
The `openapi_zerion.yaml` file SHALL include complete definitions for all webhook subscription endpoints with accurate request/response schemas.

#### Scenario: OpenAPI spec validation
- **WHEN** the OpenAPI specification is loaded by FastMCP
- **THEN** all 5 webhook endpoints are defined with:
  - Correct HTTP methods (POST, GET, PATCH, DELETE)
  - Required and optional parameters
  - Request body schemas
  - Response schemas for success (200, 201, 204) and error cases (400, 401, 404, 429)
- **AND** the spec passes OpenAPI 3.0 validation without errors

#### Scenario: MCP tool auto-generation
- **WHEN** FastMCP loads the enhanced OpenAPI spec
- **THEN** it automatically generates MCP tools for all webhook endpoints
- **AND** tool names match operation IDs (e.g., `createTxSubscription`, `listTxSubscriptions`)
- **AND** tool parameters match the OpenAPI parameter definitions
