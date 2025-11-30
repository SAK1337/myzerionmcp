# NFT Metadata Completeness Specification

## Overview

Validates and documents the completeness of NFT metadata available through Zerion API, including images, floor prices, descriptions, traits, and collection data for ERC-721 and ERC-1155 tokens.

## ADDED Requirements

### NFT Metadata Field Validation

Validate that comprehensive NFT metadata fields exist in the OpenAPI specification for NFT endpoints.

#### Scenario: Verify NFT metadata fields in OpenAPI spec

**Given** the OpenAPI specification for NFT endpoints
**When** analyzing the NFT response schema
**Then** the spec should include:
- `attributes.name` field for NFT name
- `attributes.description` field for NFT description
- `attributes.preview_url` field for image preview
- `attributes.detail_url` field for high-resolution image
- `attributes.floor_price` field for collection floor price
- `relationships.collection` relationship for collection data
- `attributes.traits` field for NFT trait data

---

### NFT Metadata Completeness Documentation

Document the comprehensive NFT metadata available through Zerion API for rich NFT displays.

#### Scenario: User reads README to understand NFT metadata

**Given** a user wants to understand NFT metadata completeness
**When** they read the README documentation
**Then** they should see a "NFT Metadata Completeness" subsection explaining that:
- Zerion provides comprehensive NFT metadata for ERC-721 and ERC-1155 tokens
- All metadata fields are documented (name, description, images, floor price, traits)
- Metadata enables rich NFT displays and galleries
- Floor price availability is noted as "where available"

---

### NFT Image Field Documentation

Document NFT image URL fields and their usage for displaying NFT visuals.

#### Scenario: User wants to display NFT images

**Given** a user is building an NFT gallery application
**When** they read the NFT image documentation
**Then** they should find documented:
- `attributes.preview_url` for thumbnail/preview images
- `attributes.detail_url` for high-resolution images
- Note that URLs may be IPFS gateways
- Image display best practices
- Image availability for most NFTs

---

### NFT Floor Price Documentation

Document floor price availability and limitations for NFT collections.

#### Scenario: User wants to display NFT floor prices

**Given** a user wants to show floor prices in their NFT application
**When** they read the floor price documentation
**Then** they should understand that:
- `attributes.floor_price` field provides collection floor price
- Floor price is available "where available"
- New/small collections may lack floor data
- Fallback UI/UX guidance is provided
- Floor price is in the specified currency denomination

---

### NFT Collection Metadata Documentation

Document NFT collection relationship data and available collection metadata.

#### Scenario: User wants to access collection data

**Given** a user wants to show NFT collection information
**When** they examine the collection metadata
**Then** they should find documented:
- `relationships.collection` structure for collection relationship
- Collection name and description fields
- Collection floor price
- Collection icon/image URL
- Distinction between collection-level and token-level metadata

---

### NFT Trait Data Documentation

Document NFT trait/attribute data for displaying NFT characteristics.

#### Scenario: User wants to display NFT traits

**Given** a user wants to show NFT traits and rarities
**When** they read the trait documentation
**Then** they should find documented:
- `attributes.traits` field structure (key-value pairs)
- Trait display examples
- Note that trait availability varies by collection
- Trait-based filtering use cases

---

### NFT Metadata Examples

Provide concrete examples showing comprehensive NFT metadata in API responses.

#### Scenario: User wants to fetch NFT with full metadata

**Given** a user wants to get complete NFT data
**When** they use `getNFTById` with an NFT ID
**Then** the example should show full metadata response including name, description, images, floor price, traits, and collection data

#### Scenario: User wants to list wallet NFTs with metadata

**Given** a user wants to display wallet NFT positions
**When** they use `listWalletNFTPositions`
**Then** the example should show NFT metadata in the response

#### Scenario: User wants to build NFT gallery

**Given** a user is building an NFT gallery application
**When** they read the NFT gallery use case
**Then** they should see a complete example showing how to use metadata for rich NFT displays

#### Scenario: User wants to build NFT marketplace UI

**Given** a user is building an NFT marketplace
**When** they read the marketplace use case
**Then** they should see examples using floor prices, images, and traits for marketplace displays

---

### NFT Metadata Limitations Documentation

Document known limitations and caveats about NFT metadata availability.

#### Scenario: User encounters missing floor price

**Given** a user queries an NFT from a small/new collection
**When** the floor price is not available
**Then** the documentation should explain:
- Floor prices may not be available for all collections
- New/small collections often lack floor data
- Metadata refresh rates and limitations
- Troubleshooting guidance for missing metadata

#### Scenario: User encounters IPFS URLs

**Given** a user receives NFT image URLs
**When** the URLs are IPFS gateways
**Then** the documentation should note:
- Image URLs may be IPFS gateways
- IPFS URL handling guidance provided
- Application may need IPFS resolution logic
