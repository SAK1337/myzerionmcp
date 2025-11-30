# Multi-Chain Aggregation Specification

## Overview

Documents the automatic multi-chain aggregation behavior of the Zerion API, which fetches data across 100+ blockchain networks in a single API call without requiring special parameters.

## ADDED Requirements

### Multi-Chain Aggregation Documentation

Document that Zerion API automatically aggregates data across 100+ blockchain networks in single API calls.

#### Scenario: User reads README to understand multi-chain capabilities

**Given** a user wants to understand Zerion's multi-chain support
**When** they read the README documentation
**Then** they should see a "Multi-Chain Aggregation" subsection explaining that:
- Zerion automatically aggregates data across 100+ blockchains
- No special parameters are needed to enable multi-chain queries
- "100+ chains in one API call" is a key differentiator
- Examples of supported chains include Ethereum, Base, Polygon, Arbitrum, Optimism, Solana

---

### Multi-Chain Aggregation Examples

Provide concrete examples showing multi-chain aggregation across portfolio, positions, and transaction endpoints.

#### Scenario: User wants to see multi-chain portfolio aggregation example

**Given** a user wants to fetch a wallet's portfolio across all chains
**When** they use the `getWalletPortfolio` tool
**Then** the documentation should show that a single call returns portfolio data aggregated across all 100+ supported chains

#### Scenario: User wants to see multi-chain position aggregation example

**Given** a user wants to fetch a wallet's positions across all chains
**When** they use the `listWalletPositions` tool
**Then** the documentation should show that a single call returns positions from all supported chains

#### Scenario: User wants to see multi-chain transaction aggregation example

**Given** a user wants to fetch a wallet's transaction history across all chains
**When** they use the `listWalletTransactions` tool
**Then** the documentation should show that a single call returns transactions from all supported chains

---

### Multi-Chain Benefits Documentation

Document the benefits of multi-chain aggregation compared to per-chain API calls.

#### Scenario: User compares Zerion to per-chain APIs

**Given** a user is evaluating Zerion vs. per-chain APIs (Alchemy, Infura, Moralis)
**When** they read the multi-chain benefits documentation
**Then** they should understand that:
- Zerion: 1 API call for portfolio across 100+ chains
- Per-chain APIs: 10+ separate API calls needed
- Reduced API quota usage with Zerion
- Simplified application logic (no manual chain aggregation)

---

### Chain Coverage Validation

Validate Zerion's chain coverage claims and document supported networks.

#### Scenario: User wants to know which chains are supported

**Given** a user wants to understand chain coverage
**When** they read the chain coverage documentation
**Then** they should see:
- "100+ chains" claim (verified from Zerion documentation)
- List of major EVM chains (Ethereum, Polygon, Arbitrum, Optimism, Base)
- List of major L2s (zkSync, StarkNet, etc.)
- Non-EVM chain support (Solana)
- Disclaimer that chain count is approximate

---

### Multi-Chain Usage Patterns

Document common usage patterns for multi-chain queries.

#### Scenario: User wants to build a cross-chain portfolio dashboard

**Given** a user is building a portfolio tracking application
**When** they read the usage patterns documentation
**Then** they should see examples for:
- Cross-chain portfolio dashboard pattern
- Multi-chain position tracking pattern
- Cross-chain transaction history pattern
- Real-world applications (DeFi aggregators, portfolio trackers)
