# DeFi Protocol Coverage Specification

## Overview

Validates and documents the availability of DeFi protocol metadata in Zerion API responses, including protocol relationships and position type data for 8,000+ tracked protocols.

## ADDED Requirements

### Protocol Relationship Field Validation

Validate that `relationships.protocol` data exists in position API responses and document the available fields.

#### Scenario: Verify protocol relationship structure in OpenAPI spec

**Given** the OpenAPI specification for position endpoints
**When** analyzing the response schema
**Then** the spec should include:
- `relationships.protocol.data.id` field for protocol identifier
- Protocol data following JSON:API relationship format
- Protocol relationship included in position responses

---

### Protocol Metadata Field Documentation

Document all protocol metadata fields available in API responses.

#### Scenario: User wants to access protocol metadata

**Given** a user receives position data from the API
**When** they examine the protocol metadata fields
**Then** they should find documented:
- `relationships.protocol.data.id` (e.g., "uniswap-v3")
- `attributes.protocol.name` (human-readable protocol name)
- `attributes.protocol.icon_url` (protocol logo URL)
- `attributes.position_type` (staked, deposit, loan, reward, etc.)

---

### DeFi Protocol Coverage Documentation

Document Zerion's tracking of 8,000+ DeFi protocols and explain protocol metadata availability.

#### Scenario: User reads README to understand protocol coverage

**Given** a user wants to understand DeFi protocol support
**When** they read the README documentation
**Then** they should see a "DeFi Protocol Coverage" subsection explaining that:
- Zerion tracks 8,000+ DeFi protocols
- Protocol metadata is included in position responses
- Available fields include protocol ID, name, icon, position type
- JSON:API relationship structure is used
- Protocol count is approximate (disclaimer included)

---

### DeFi Protocol Examples

Provide concrete examples showing protocol metadata in position responses.

#### Scenario: User wants to see Uniswap LP position with protocol data

**Given** a user queries wallet positions using `listWalletPositions`
**When** the response includes Uniswap LP positions
**Then** the example should show protocol relationship data with Uniswap protocol metadata

#### Scenario: User wants to see Aave lending position with protocol data

**Given** a user queries wallet positions
**When** the response includes Aave lending positions
**Then** the example should show protocol relationship data with Aave protocol metadata

#### Scenario: User wants to filter positions by protocol

**Given** a user wants to see only Uniswap positions
**When** they use `filter[protocol_ids]` parameter
**Then** the example should show how to filter for specific protocols

#### Scenario: User wants to build DeFi analytics

**Given** a user is building a DeFi analytics dashboard
**When** they read the usage patterns
**Then** they should see examples for protocol-based analytics use cases

---

### Protocol Filtering Validation

Validate that `filter[protocol_ids]` parameter exists for filtering positions by protocol.

#### Scenario: Verify protocol filtering in OpenAPI spec

**Given** the OpenAPI specification for `listWalletPositions` endpoint
**When** analyzing the query parameters
**Then** the spec should include `filter[protocol_ids]` parameter with:
- Parameter documented in spec
- Support for multi-protocol filtering
- Usage examples provided

---

### Protocol Categories Documentation

Document examples of protocol categories and major protocols in each category.

#### Scenario: User wants to understand protocol categories

**Given** a user wants to see what types of DeFi protocols are tracked
**When** they read the protocol categories documentation
**Then** they should see examples including:
- DEX protocols: Uniswap, Curve, Balancer, SushiSwap
- Lending protocols: Aave, Compound, MakerDAO
- Staking protocols: Lido, Rocket Pool
- Yield aggregators: Yearn, Beefy
- Summary: "8,000+ total protocols"

---

### Protocol Data Usage Patterns

Document common usage patterns for DeFi protocol data.

#### Scenario: User wants to build protocol analytics dashboard

**Given** a user is building a DeFi application
**When** they read the usage patterns documentation
**Then** they should see examples for:
- Protocol analytics dashboard pattern
- DeFi position aggregation by protocol
- Protocol yield tracking pattern
- Real-world DeFi analytics tools
