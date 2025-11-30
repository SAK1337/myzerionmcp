# Webhook Support Design Document

## Context

The Zerion MCP Server currently provides read-only access to portfolio, transaction, NFT, and market data through auto-generated MCP tools from an OpenAPI specification. However, the server lacks webhook/transaction subscription capabilities, which are critical for:

1. **Real-time notifications**: Applications need immediate updates when wallet transactions occur
2. **Rate limit conservation**: Polling wastes API quota; webhooks provide event-driven updates
3. **Production viability**: 80% of advanced use cases (mobile alerts, trading bots, SocialFi) require webhooks

### Stakeholders
- **MCP Server Users**: Developers building AI applications that need real-time crypto data
- **End Users**: Applications requiring wallet activity notifications
- **Zerion API**: Upstream API provider with webhook capabilities

### Constraints
- MCP servers run in **stdio mode** for AI assistant integration (Claude Desktop)
- Webhooks require **HTTP endpoints** to receive POST callbacks
- FastMCP auto-generates tools from OpenAPI specs; custom tool logic should be avoided
- Zerion OpenAPI spec hosted on GitHub does not currently include webhook endpoints

---

## Goals / Non-Goals

### Goals
✅ Expose all 5 webhook subscription CRUD endpoints as MCP tools
✅ Enable users to manage transaction subscriptions programmatically
✅ Document webhook setup workflow clearly (including external receiver requirement)
✅ Provide comprehensive filter parameter documentation for existing endpoints
✅ Maintain backward compatibility (no breaking changes)

### Non-Goals
❌ Build a webhook receiver service within the MCP server (architectural mismatch)
❌ Implement webhook signature verification in MCP server (user's receiver responsibility)
❌ Create a unified stdio+HTTP hybrid MCP server
❌ Modify FastMCP framework behavior

---

## Decisions

### Decision 1: OpenAPI Spec Extension Strategy

**Choice**: Extend the local `openapi_zerion.yaml` file with webhook endpoint definitions based on Zerion's official documentation.

**Rationale**:
- Upstream spec (GitHub) does not include webhooks, so we must define them ourselves
- FastMCP auto-generates tools from OpenAPI, so spec updates automatically expose tools
- Spec-driven approach maintains consistency with existing architecture
- Future upstream updates can be merged if Zerion adds webhook endpoints to official spec

**Alternatives Considered**:
1. ❌ **Custom tool implementation**: Would bypass FastMCP's auto-generation, creating maintenance burden
2. ❌ **Fork upstream spec repo**: Adds Git submodule complexity and merge conflicts
3. ❌ **Wait for upstream**: Blocks critical functionality indefinitely

**Implementation**:
- Add webhook paths to `paths:` section of `openapi_zerion.yaml`
- Define request/response schemas in `components/schemas`
- Follow Zerion API documentation for accurate field definitions
- Use operation IDs like `createTxSubscription`, `listTxSubscriptions`, etc.

---

### Decision 2: Webhook Receiver Architecture

**Choice**: Document that users must deploy a **separate HTTP webhook receiver service** external to the MCP server.

**Rationale**:
- MCP servers run in stdio mode (stdin/stdout communication with AI assistants)
- Mixing stdio and HTTP modes creates architectural complexity and deployment confusion
- Separation of concerns: MCP server manages subscriptions; user's service receives events
- Users have flexibility to deploy receivers in their own infrastructure (cloud functions, servers, etc.)

**Flow Diagram**:
```
┌──────────────┐
│  AI Client   │ (e.g., Claude Desktop)
│              │
└──────┬───────┘
       │ stdio (MCP protocol)
       ▼
┌──────────────┐
│  MCP Server  │
│  (stdio)     │
└──────┬───────┘
       │ HTTPS (manage subscriptions)
       ▼
┌──────────────┐
│  Zerion API  │
└──────┬───────┘
       │ Webhooks (HTTP POST)
       ▼
┌──────────────┐
│ User's HTTP  │ (separate service)
│   Receiver   │
└──────────────┘
```

**Alternatives Considered**:
1. ❌ **Hybrid stdio+HTTP MCP server**: Adds complexity, confuses deployment, breaks MCP conventions
2. ❌ **Embed HTTP server in MCP**: Requires threading/async complexity, port management, firewall issues
3. ❌ **Polling-based MCP tools**: Defeats purpose of webhooks (wastes quota, adds latency)

**Implementation**:
- Document webhook receiver requirement prominently in README
- Provide example receiver implementations (Python Flask, Node Express, etc.)
- Recommend webhook.site for testing before production deployment
- Explain callback URL must be publicly accessible HTTPS endpoint

---

### Decision 3: Filter Parameter Documentation Approach

**Choice**: Add comprehensive "Advanced Filtering" section to README with examples, use cases, and applicability matrix.

**Rationale**:
- Filters already exist in OpenAPI spec but are not discoverable or documented
- Users waste quota fetching unfiltered data then filtering client-side
- DeFi analytics require `only_complex` filter but users don't know it exists
- Matrix table prevents trial-and-error testing of filter compatibility

**Content Strategy**:
- One subsection per major filter type (positions, chain_ids, trash, operation_types, position_types)
- Each subsection includes: parameter syntax, use case, example, expected response
- Filter applicability matrix table showing which endpoints support which filters
- Query optimization section explaining quota/performance impact

**Alternatives Considered**:
1. ❌ **Auto-generate docs from OpenAPI**: Loses context, examples, and use case explanations
2. ❌ **Link to Zerion docs**: External dependency, fragmented experience, may not be MCP-specific
3. ❌ **In-code comments only**: Not accessible to end users reading README

---

### Decision 4: Testing Strategy

**Choice**: Integration tests for webhook CRUD operations using mock HTTP responses (respx library).

**Rationale**:
- Can't test actual webhook delivery without running external receiver
- Can verify MCP tools correctly call Zerion API with proper parameters/headers
- Mock testing is fast and doesn't consume API quota
- Manual testing with webhook.site for end-to-end validation

**Test Coverage**:
- Create subscription: Verify request body, headers, response parsing
- List subscriptions: Verify pagination, empty state
- Update subscription: Verify PATCH semantics
- Delete subscription: Verify 204 handling, idempotency
- Error cases: 400, 401, 404, 429 responses

**Alternatives Considered**:
1. ❌ **Live API testing only**: Consumes quota, requires test API key, slow
2. ❌ **No testing**: Unacceptable for production feature
3. ❌ **E2E webhook delivery tests**: Requires complex infrastructure setup

---

## Risks / Trade-offs

### Risk 1: OpenAPI Spec Drift from Upstream

**Description**: Our manually extended `openapi_zerion.yaml` may diverge from Zerion's actual API behavior if they change webhook endpoints.

**Mitigation**:
- Document spec version and last-updated date in comments
- Periodically check Zerion changelog for webhook API changes
- Add integration tests that fail if API responses don't match spec
- If Zerion publishes official webhook spec, merge and deprecate our custom definitions

**Severity**: Medium (fixable with spec updates)

---

### Risk 2: Webhook Receiver Setup Complexity

**Description**: Users may struggle to deploy and configure webhook receiver services, especially non-technical AI assistant users.

**Mitigation**:
- Provide step-by-step setup guide with screenshots
- Include ready-to-deploy receiver examples (Vercel/Netlify serverless functions)
- Recommend webhook.site for testing before production
- Create troubleshooting checklist for common issues (HTTPS, public URL, firewall)

**Severity**: High (impacts adoption)

---

### Risk 3: Rate Limiting on Subscription Management

**Description**: Zerion may rate-limit subscription CRUD operations separately from data endpoints.

**Mitigation**:
- Document rate limits based on Zerion docs
- Implement exponential backoff in error handling (future enhancement)
- Advise users to manage subscriptions infrequently (setup once, long-lived)

**Severity**: Low (subscriptions are infrequent operations)

---

### Risk 4: Filter Parameter Confusion

**Description**: Users may try to use filters on unsupported endpoints, leading to frustration when parameters are ignored.

**Mitigation**:
- Applicability matrix table clearly shows which filters work on which endpoints
- Document API behavior when unsupported filters are passed (ignored vs. error)
- Provide clear error messages in examples

**Severity**: Medium (UX issue, not technical blocker)

---

## Migration Plan

### Phase 1: OpenAPI Spec Update
1. Research Zerion webhook API from official docs and blog posts
2. Define webhook endpoint schemas in `openapi_zerion.yaml`
3. Validate spec with OpenAPI linter
4. Test that FastMCP auto-generates tools correctly

### Phase 2: Documentation
1. Add "Webhooks" section to README with setup guide
2. Add "Advanced Filtering" section with filter docs
3. Create webhook receiver examples (Python, Node.js)
4. Add troubleshooting section

### Phase 3: Testing
1. Write integration tests for webhook CRUD
2. Manual testing with live API and webhook.site
3. Validate all examples in documentation work

### Phase 4: Release
1. Update CHANGELOG.md
2. Tag release (e.g., v0.2.0 - Add Webhook Support)
3. Announce new capabilities in README

### Rollback Plan
If webhook implementation causes issues:
1. Revert `openapi_zerion.yaml` changes
2. FastMCP will stop generating webhook tools
3. Existing portfolio/transaction tools unaffected (backward compatible)

---

## Open Questions

### Q1: Does Zerion support webhook signature verification?
**Status**: Research needed from Zerion docs
**Impact**: Security best practice for production webhooks
**Action**: Document if supported; otherwise note as future enhancement

### Q2: Are there webhook quota limits (max subscriptions per API key)?
**Status**: Not documented in available research
**Impact**: Users may hit limits unexpectedly
**Action**: Document known limits; recommend contacting Zerion for enterprise needs

### Q3: Can subscriptions monitor wildcard addresses or address patterns?
**Status**: Assume no based on docs (explicit address array required)
**Impact**: Users must create subscriptions per address
**Action**: Document limitation; suggest batching addresses in single subscription

### Q4: What is the webhook retry policy and timeout?
**Status**: Partially documented (3 retries mentioned in research)
**Impact**: Receiver service must respond quickly
**Action**: Document retry behavior and recommend < 5 second response times

---

## Success Metrics

- ✅ All 5 webhook endpoints exposed as MCP tools
- ✅ At least 3 documented webhook examples (EVM, Solana, multi-wallet)
- ✅ Filter parameter documentation covers 6+ filter types
- ✅ Integration test coverage > 80% for webhook CRUD operations
- ✅ Zero breaking changes to existing tools
- ✅ Webhook setup guide is under 500 words (concise and actionable)

---

## References

- [Zerion API Documentation](https://developers.zerion.io/)
- [FastMCP OpenAPI Integration](https://github.com/jlowin/fastmcp)
- [OpenAPI 3.0 Specification](https://spec.openapis.org/oas/v3.0.3)
- Gap Analysis Document (GapAnalysis.md in project root)
