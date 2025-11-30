# Feature Parity Validation Design

## Context

The Zerion MCP Server uses FastMCP to auto-generate tools from the OpenAPI specification. This means that if a parameter exists in `openapi_zerion.yaml`, FastMCP should automatically expose it as a tool parameter. However, the GapAnalysis Section 3 shows many features marked as "Unknown" status.

The gap is not implementation but **validation and documentation** - we need to confirm FastMCP correctly exposes these parameters and document how to use them.

## Goals / Non-Goals

### Goals
✅ Validate filter parameters work as expected
✅ Validate testnet header (X-Env) works
✅ Validate currency parameter works
✅ Document all validated features with examples
✅ Create validation test suite

### Non-Goals
❌ Modify OpenAPI spec (use as-is)
❌ Add custom parameter injection logic
❌ Implement client-side filtering
❌ Add new API endpoints

## Decisions

### Decision 1: Validation Approach

**Choice**: Test with real API calls to Zerion, not mocked responses.

**Rationale**:
- Need to confirm FastMCP parameter passing works end-to-end
- OpenAPI spec may have parameters that API doesn't actually support
- Real API responses reveal actual behavior vs. spec documentation
- Validates both MCP server AND API behavior

**Implementation**:
```python
# Example validation test
async def test_chain_filter_parameter():
    # Use listWalletPositions with filter[chain_ids]=ethereum
    response = await client.request(
        "GET",
        "/v1/wallets/0x.../positions",
        params={"filter[chain_ids]": "ethereum"}
    )

    # Verify only Ethereum positions returned
    for position in response["data"]:
        chain = position["relationships"]["chain"]["id"]
        assert chain == "ethereum"
```

**Alternatives Considered**:
1. ❌ **Mock validation**: Doesn't prove FastMCP parameter passing works
2. ❌ **OpenAPI spec analysis only**: Spec may be incomplete or wrong
3. ✅ **Real API testing**: Highest confidence validation

### Decision 2: Documentation Structure

**Choice**: Create dedicated filtering guide section in README between "Advanced Filtering" and existing operational sections.

**Rationale**:
- README already has "Advanced Filtering - Query Optimization" section
- Need to enhance it with validated parameter examples
- Users need concrete examples, not just parameter lists
- Should show combinations of filters for common use cases

**Implementation**:
Enhance existing filtering section with:
- Parameter reference table (parameter → endpoints → purpose)
- 15+ concrete examples with expected results
- Common filter combinations for use cases
- Testnet examples with X-Env header
- Currency parameter examples

**Alternatives Considered**:
1. ❌ **Separate FILTERS.md file**: Fragments documentation
2. ❌ **Inline in each function**: Repeats examples
3. ✅ **Enhanced README section**: Centralized, discoverable

### Decision 3: X-Env Testnet Header Validation

**Choice**: Document X-Env as optional parameter for applicable tools, validate with testnet API key.

**Rationale**:
- OpenAPI spec shows X-Env header on specific endpoints (positions, portfolio, transactions, NFTs)
- FastMCP should pass headers through to API
- Users need testnet API access to validate (may not be available)
- Documentation must clarify which endpoints support testnets

**Implementation**:
```markdown
### Testnet Support

Certain endpoints support testnet data via the `X-Env` header:

Supported endpoints:
- listWalletPositions
- getWalletPortfolio
- listWalletTransactions
- listWalletNFTPositions

Example:
Use listWalletPositions with:
- address: "0x..."
- X-Env: "testnet"
```

**Validation Plan**:
- Test if FastMCP passes X-Env header to API
- Document in README even if we can't test with real testnet data
- Mark as "Documented but not validated" in Feature Parity Matrix if no testnet key available

## Risks / Trade-offs

### Risk 1: Testnet API Access

**Description**: We may not have testnet API credentials to fully validate X-Env header.

**Mitigation**:
- Document the parameter based on OpenAPI spec
- Add note that testnet validation requires testnet-enabled API key
- Mark feature as "Documented" in parity matrix
- Encourage community validation

**Severity**: Low (documentation still valuable)

### Risk 2: Filter Parameters May Not Work as Expected

**Description**: OpenAPI spec may list parameters that API ignores or handles differently.

**Mitigation**:
- Test each parameter with real API calls
- Document actual behavior vs. spec claims
- Report discrepancies to Zerion or update local spec
- Mark validated vs. unvalidated parameters clearly

**Severity**: Medium (requires careful validation)

### Risk 3: Breaking Changes from Future API Updates

**Description**: Documented filters may change in future Zerion API versions.

**Mitigation**:
- Version-pin OpenAPI spec URL in code
- Add "Last validated: 2025-11-30" timestamps to docs
- Create validation test suite that can be re-run on API updates
- Monitor Zerion changelog for breaking changes

**Severity**: Low (standard API versioning risk)

## Migration Plan

### Phase 1: Parameter Validation
1. Create validation test script
2. Test each filter parameter with real API
3. Test X-Env header with available credentials
4. Test currency parameter (usd, eth, eur, btc)
5. Document actual behavior

### Phase 2: Documentation
1. Update README filtering section
2. Add parameter reference table
3. Add 15+ concrete examples
4. Add testnet section
5. Add currency examples

### Phase 3: Testing
1. Create automated validation tests
2. Add to test suite
3. Run full test suite
4. Update Feature Parity Matrix

### Phase 4: Validation
1. Run validation tests
2. Update Feature Parity Matrix with results
3. Mark validated features as ✅
4. Document any discrepancies found

## Success Metrics

- ✅ 90%+ of filter parameters validated and documented
- ✅ X-Env header documented with usage examples
- ✅ Currency parameter validated for all supported currencies
- ✅ 15+ filter examples in README
- ✅ Validation test suite created
- ✅ Feature Parity Matrix updated
- ✅ Zero breaking changes to existing functionality

## Open Questions

### Q1: Do we have testnet API credentials?
**Status**: Unknown
**Impact**: May limit X-Env validation
**Action**: Check with user or document parameter without full validation

### Q2: Which filter combinations are most valuable?
**Status**: Needs user research
**Options**: Focus on examples from GapAnalysis use cases
**Action**: Prioritize DeFi filtering, spam filtering, chain filtering

### Q3: Should we create filter helper functions?
**Status**: Out of scope for validation
**Impact**: Would improve UX but adds complexity
**Action**: Document in future enhancement backlog
