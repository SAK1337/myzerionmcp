# Implementation Tasks

## 1. OpenAPI Specification Enhancement
- [x] 1.1 Research Zerion webhook API endpoints from official documentation
- [x] 1.2 Define OpenAPI schema for `POST /v1/tx-subscriptions` (create subscription)
- [x] 1.3 Define OpenAPI schema for `GET /v1/tx-subscriptions` (list subscriptions)
- [x] 1.4 Define OpenAPI schema for `GET /v1/tx-subscriptions/{id}` (get subscription)
- [x] 1.5 Define OpenAPI schema for `PATCH /v1/tx-subscriptions/{id}` (update subscription)
- [x] 1.6 Define OpenAPI schema for `DELETE /v1/tx-subscriptions/{id}` (delete subscription)
- [x] 1.7 Add webhook request/response schemas to components section
- [x] 1.8 Add subscription object schema with attributes (addresses, callback_url, chain_ids)
- [x] 1.9 Validate OpenAPI spec syntax with linter/validator

## 2. MCP Tool Exposure
- [x] 2.1 Verify FastMCP auto-generates tools from updated OpenAPI spec
- [x] 2.2 Test tool discovery in MCP client (Claude Desktop)
- [x] 2.3 Confirm tool parameters match OpenAPI definitions

## 3. Documentation - Webhook Guide
- [x] 3.1 Add "Webhooks" section to README.md
- [x] 3.2 Document webhook subscription creation workflow
- [x] 3.3 Provide example: Create subscription for Ethereum address
- [x] 3.4 Provide example: Create subscription for Solana address
- [x] 3.5 Document webhook payload structure (based on Zerion docs)
- [x] 3.6 Add security note about webhook signature verification
- [x] 3.7 Document webhook receiver setup (external HTTP service requirement)
- [x] 3.8 Add troubleshooting section for common webhook issues

## 4. Documentation - Filter Parameters
- [x] 4.1 Add "Advanced Filtering" section to README.md
- [x] 4.2 Document `filter[positions]=only_complex` with DeFi use case example
- [x] 4.3 Document `filter[chain_ids]` with cross-chain query example
- [x] 4.4 Document `filter[trash]` with spam filtering example
- [x] 4.5 Document `filter[operation_types]` with transaction type filtering example
- [x] 4.6 Document `filter[position_types]` with position categorization example
- [x] 4.7 Create comparison table showing which filters apply to which endpoints
- [x] 4.8 Add "Query Optimization" section explaining filter impact on quota usage

## 5. Configuration Examples
- [x] 5.1 Add webhook callback URL configuration example to config.yaml
- [x] 5.2 Update .env.example with WEBHOOK_CALLBACK_URL placeholder
- [x] 5.3 Document environment variable options for webhook testing

## 6. Testing
- [x] 6.1 Create integration test for webhook subscription creation
- [x] 6.2 Create integration test for listing subscriptions
- [x] 6.3 Create integration test for updating subscription
- [x] 6.4 Create integration test for deleting subscription
- [x] 6.5 Add test fixtures for webhook payloads
- [x] 6.6 Document manual testing procedure with webhook.site

## 7. Validation & Quality Assurance
- [x] 7.1 Test all webhook endpoints against live Zerion API (with test key)
- [x] 7.2 Verify MCP tools correctly expose all parameters
- [x] 7.3 Validate documentation examples are copy-paste ready
- [x] 7.4 Review with actual webhook receiver service
- [x] 7.5 Run full test suite with coverage report
- [x] 7.6 Update CHANGELOG.md with webhook feature addition

## Dependencies & Sequencing
- Tasks 1.x must complete before 2.x (need spec for tool generation)
- Tasks 2.x must complete before 6.x (need tools for testing)
- Tasks 3.x and 4.x can run in parallel (independent documentation)
- Task 7.x runs after all implementation tasks complete

## Success Criteria
- ✅ All 5 webhook endpoints exposed as MCP tools
- ✅ Documentation includes at least 3 working webhook examples
- ✅ Filter parameter documentation covers all major use cases
- ✅ Integration tests pass for all CRUD operations
- ✅ README clearly explains webhook receiver setup requirements
