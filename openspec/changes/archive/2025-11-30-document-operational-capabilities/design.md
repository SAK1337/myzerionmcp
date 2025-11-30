# Operational Capabilities Documentation Design

## Context

The Zerion MCP Server leverages Zerion's API which provides three key operational capabilities that differentiate it from competitors:

1. **Multi-Chain Aggregation** - Single API call returns data across 100+ blockchains
2. **DeFi Protocol Coverage** - 8,000+ protocols with detailed position breakdowns
3. **NFT Metadata Richness** - Complete metadata including images, floor prices, descriptions

These capabilities already work through FastMCP but are not documented, validated, or highlighted to users.

## Goals / Non-Goals

### Goals
✅ Document multi-chain aggregation behavior
✅ Validate DeFi protocol metadata availability
✅ Validate NFT metadata completeness
✅ Create concrete usage examples
✅ Highlight competitive advantages

### Non-Goals
❌ Add new API endpoints
❌ Modify API response structure
❌ Implement custom protocol parsing
❌ Create NFT metadata enrichment

## Decisions

### Decision 1: Multi-Chain Documentation Approach

**Choice**: Document multi-chain as inherent API behavior, not as a feature to "enable".

**Rationale**:
- Zerion API aggregates chains automatically
- No special parameters needed to enable multi-chain
- Key differentiator: "One API call, 100+ chains"
- Users should understand this reduces API quota usage vs. per-chain APIs

**Implementation**:
```markdown
### Multi-Chain Aggregation

Zerion automatically aggregates data across **100+ blockchain networks** in a single API call.
No special parameters needed - multi-chain support is built-in.

Example: Get portfolio across all chains
Use getWalletPortfolio with:
- address: "0x..."
- currency: "usd"

Result: Portfolio value aggregated from Ethereum, Base, Polygon, Arbitrum,
Optimism, Solana, and 100+ other chains in one response.
```

**Alternatives Considered**:
1. ❌ **Add chain aggregation parameter**: Not needed, always enabled
2. ❌ **Document per-chain queries**: Would miss the key advantage
3. ✅ **Highlight automatic aggregation**: Shows value proposition

### Decision 2: DeFi Protocol Metadata Validation

**Choice**: Validate that `relationships.protocol` data exists in position responses and document available fields.

**Rationale**:
- API responses include relationship data (per JSON:API spec)
- Protocol metadata enables DeFi analytics
- 8,000+ protocols tracked by Zerion
- Users need to know this data is available

**Implementation**:
```markdown
### DeFi Protocol Coverage

Zerion tracks **8,000+ DeFi protocols** and includes protocol metadata in position responses:

Available Protocol Data:
- relationships.protocol.data.id - Protocol identifier (e.g., "uniswap-v3")
- attributes.protocol.name - Human-readable name
- attributes.protocol.icon_url - Protocol logo
- attributes.position_type - Type (staked, deposit, loan, reward, etc.)

Example: Get LP positions with protocol data
Use listWalletPositions with:
- address: "0x..."
- filter[positions]: "only_complex"

Response includes protocol relationships for Uniswap, Aave, Curve, etc.
```

**Validation Method**:
- Examine OpenAPI spec for protocol fields
- Check existing responses for protocol relationship structure
- Document all available protocol metadata fields

**Alternatives Considered**:
1. ❌ **Implement custom protocol enrichment**: Out of scope
2. ❌ **Create protocol mapping**: Zerion already provides this
3. ✅ **Document existing protocol data**: Shows what's available

### Decision 3: NFT Metadata Completeness Validation

**Choice**: Validate NFT metadata fields in API responses and document completeness.

**Rationale**:
- NFT endpoints exist but metadata completeness unclear
- Floor prices, images, descriptions critical for NFT apps
- Users need to know data richness for UI/UX decisions

**Implementation**:
```markdown
### NFT Metadata Completeness

Zerion provides comprehensive NFT metadata for ERC-721 and ERC-1155 tokens:

Available NFT Metadata:
- attributes.name - Token name
- attributes.description - Token description
- attributes.preview_url - Image preview URL
- attributes.detail_url - High-resolution image URL
- attributes.floor_price - Collection floor price (where available)
- relationships.collection - Collection metadata
- attributes.traits - NFT trait data

Example: Get NFT with full metadata
Use getNFTById with:
- nft_id: "ethereum:0x...:{token_id}"

Response includes complete metadata for rich NFT displays.
```

**Validation Method**:
- Check OpenAPI spec for NFT response schema
- Verify floor_price field availability
- Confirm image URL fields exist
- Document metadata completeness

## Risks / Trade-offs

### Risk 1: API Response Structure Changes

**Description**: Zerion may change response structure, invalidating documentation.

**Mitigation**:
- Base documentation on OpenAPI spec (canonical source)
- Add "Last validated" timestamps
- Version-pin OpenAPI spec URL
- Monitor Zerion changelog

**Severity**: Low (standard API versioning risk)

### Risk 2: Protocol Coverage Claims

**Description**: Claiming "8,000+" protocols may become outdated.

**Mitigation**:
- Use "8,000+" instead of exact number
- Cite Zerion's own marketing claims
- Add disclaimer about protocol count being approximate
- Reference Zerion documentation

**Severity**: Low (common in API documentation)

### Risk 3: NFT Metadata Availability

**Description**: Floor prices may not be available for all collections.

**Mitigation**:
- Document as "where available"
- Explain floor price limitations
- Note that new/small collections may lack floor data
- Provide fallback UI/UX guidance

**Severity**: Low (clearly document limitations)

## Migration Plan

### Phase 1: Validation
1. Analyze OpenAPI spec for protocol and NFT metadata fields
2. Verify multi-chain behavior through spec analysis
3. Document available fields and data structures

### Phase 2: Documentation
1. Create "Operational Capabilities" section in README
2. Add multi-chain aggregation subsection
3. Add DeFi protocol coverage subsection
4. Add NFT metadata completeness subsection
5. Add 10+ concrete examples

### Phase 3: Examples
1. Create multi-chain query examples
2. Create DeFi protocol filtering examples
3. Create NFT metadata display examples
4. Show competitive advantages

### Phase 4: Validation
1. Validate documentation accuracy
2. Update GapAnalysis.md Section 4
3. Mark operational capabilities as documented
4. Run OpenSpec validation

## Success Metrics

- ✅ Multi-chain aggregation documented with 3+ examples
- ✅ DeFi protocol coverage documented with available fields
- ✅ NFT metadata completeness documented with all fields
- ✅ 10+ concrete usage examples
- ✅ README "Operational Capabilities" section complete
- ✅ GapAnalysis Section 4 updated with validation results

## Open Questions

### Q1: Do we have access to real API responses for validation?
**Status**: Not critical - can validate via OpenAPI spec
**Impact**: Documentation based on spec is sufficient
**Action**: Use OpenAPI spec as canonical source

### Q2: Should we create code examples for protocol parsing?
**Status**: Out of scope for documentation
**Impact**: Users can parse JSON:API responses directly
**Action**: Document fields, not parsing implementation

### Q3: How to handle NFT image URLs that may be IPFS?
**Status**: Document as-is
**Impact**: Users handle IPFS resolution in their apps
**Action**: Note that URLs may be IPFS gateways
