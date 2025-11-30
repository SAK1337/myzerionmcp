# filter-validation Specification

## Purpose
TBD - created by archiving change validate-feature-parity. Update Purpose after archive.
## Requirements
### Requirement: Chain Filtering Validation
The MCP server SHALL validate that `filter[chain_ids]` parameter works correctly for filtering results by blockchain and document its usage with examples.

#### Scenario: Single chain filter on positions
- **WHEN** user calls `listWalletPositions` with `filter[chain_ids]=ethereum`
- **THEN** all returned positions belong to Ethereum chain only
- **AND** positions from other chains (Polygon, Base, etc.) are excluded
- **AND** response data validates successfully

#### Scenario: Multiple chain filter
- **WHEN** user calls `listWalletTransactions` with `filter[chain_ids]=ethereum,base`
- **THEN** all returned transactions belong to either Ethereum or Base chains
- **AND** transactions from other chains are excluded
- **AND** documentation includes this example

#### Scenario: Chain filter documentation
- **WHEN** user reads filter documentation in README
- **THEN** they find `filter[chain_ids]` parameter explained
- **AND** they find 3+ concrete examples with different chains
- **AND** they find list of valid chain IDs

---

### Requirement: Position Type Filtering Validation
The MCP server SHALL validate that `filter[positions]` parameter works correctly for isolating DeFi positions from simple balances and document its critical use cases.

#### Scenario: DeFi-only positions filter
- **WHEN** user calls `listWalletPositions` with `filter[positions]=only_complex`
- **THEN** only DeFi protocol positions are returned (staking, LP, lending)
- **AND** simple fungible token balances are excluded
- **AND** response includes relationship data for protocols

#### Scenario: Simple balances filter
- **WHEN** user calls `listWalletPositions` with `filter[positions]=only_simple`
- **THEN** only wallet-type positions are returned (simple token balances)
- **AND** DeFi positions are excluded

#### Scenario: No position filter
- **WHEN** user calls `listWalletPositions` with `filter[positions]=no_filter`
- **THEN** both simple and complex positions are returned
- **AND** response includes all position types

#### Scenario: Position filter documentation
- **WHEN** user reads DeFi filtering documentation
- **THEN** they find `filter[positions]=only_complex` explained as critical feature
- **AND** they find institutional use case examples (risk management, accounting)
- **AND** they understand difference between simple and complex positions

---

### Requirement: Spam Filtering Validation
The MCP server SHALL validate that `filter[trash]` parameter works correctly for hiding spam tokens and document its usage for clean transaction histories.

#### Scenario: Hide spam transactions
- **WHEN** user calls `listWalletTransactions` with `filter[trash]=only_non_trash`
- **THEN** spam and dust transactions are excluded from results
- **AND** only legitimate transactions are returned
- **AND** transaction count is significantly reduced for wallets with spam

#### Scenario: Show only spam
- **WHEN** user calls `listWalletTransactions` with `filter[trash]=only_trash`
- **THEN** only spam and dust transactions are returned
- **AND** legitimate transactions are excluded
- **AND** security monitoring use case is documented

#### Scenario: No trash filter
- **WHEN** user calls `listWalletTransactions` with `filter[trash]=no_filter`
- **THEN** all transactions are returned including spam

#### Scenario: Spam filter documentation
- **WHEN** user reads spam filtering documentation
- **THEN** they find `filter[trash]=only_non_trash` recommended for user-facing apps
- **AND** they find examples for clean transaction histories
- **AND** they understand spam impact on response size

---

### Requirement: Transaction Type Filtering Validation
The MCP server SHALL validate that `filter[operation_types]` parameter works correctly for isolating specific transaction categories.

#### Scenario: Filter for trades only
- **WHEN** user calls `listWalletTransactions` with `filter[operation_types]=trade`
- **THEN** only DEX swaps and trades are returned
- **AND** transfers, approvals, and contract executions are excluded

#### Scenario: Filter for multiple operation types
- **WHEN** user calls `listWalletTransactions` with `filter[operation_types]=trade,transfer`
- **THEN** only trades and transfers are returned
- **AND** other operation types are excluded

#### Scenario: Operation types documentation
- **WHEN** user reads transaction filtering documentation
- **THEN** they find complete list of valid operation_types (trade, transfer, execute, approve, deposit, withdraw)
- **AND** they find use case examples for trading analytics
- **AND** they find examples for transfer tracking

---

### Requirement: DeFi Position Type Filtering Validation
The MCP server SHALL validate that `filter[position_types]` parameter works correctly for granular DeFi position categorization.

#### Scenario: Filter for staked positions
- **WHEN** user calls `listWalletPositions` with `filter[positions]=only_complex` and `filter[position_types]=staked`
- **THEN** only staked token positions are returned
- **AND** lending, LP, and other position types are excluded

#### Scenario: Filter for rewards
- **WHEN** user calls `listWalletPositions` with `filter[position_types]=reward`
- **THEN** only claimable reward positions are returned

#### Scenario: Multiple position types
- **WHEN** user calls `listWalletPositions` with `filter[position_types]=staked,reward`
- **THEN** both staked positions and rewards are returned
- **AND** other position types are excluded

#### Scenario: Position types documentation
- **WHEN** user reads position type filtering documentation
- **THEN** they find complete list of position_types (wallet, deposit, loan, staked, reward, locked, margin, airdrop)
- **AND** they find use cases for staking dashboards and yield optimization

---

### Requirement: Filter Combination Validation
The MCP server SHALL validate that multiple filters can be combined effectively and document common filter combinations for real-world use cases.

#### Scenario: DeFi + Chain + No Spam filter
- **WHEN** user calls `listWalletPositions` with `filter[positions]=only_complex`, `filter[chain_ids]=ethereum`, and `filter[trash]=only_non_trash`
- **THEN** only DeFi positions on Ethereum without spam are returned
- **AND** response is optimized for risk dashboard use case

#### Scenario: L2 Trading Analytics filter
- **WHEN** user calls `listWalletTransactions` with `filter[chain_ids]=base,optimism,arbitrum`, `filter[operation_types]=trade`, and `filter[trash]=only_non_trash`
- **THEN** only clean trading activity on Layer 2 chains is returned

#### Scenario: Staking Tracker filter
- **WHEN** user calls `listWalletPositions` with `filter[positions]=only_complex` and `filter[position_types]=staked,reward`
- **THEN** only staking positions and rewards are returned

#### Scenario: Filter combination documentation
- **WHEN** user reads common filter combinations section
- **THEN** they find 5+ real-world use case examples
- **AND** each example shows filter combination and expected result
- **AND** they find quota optimization guidance

---

### Requirement: Filter Parameter Reference Documentation
The README SHALL include comprehensive filter parameter reference table mapping parameters to endpoints and providing usage guidance.

#### Scenario: Filter reference table
- **WHEN** user reads filter parameters section
- **THEN** they find table showing which filters apply to which endpoints
- **AND** table includes filter name, applicable endpoints, and purpose
- **AND** table is easy to scan for their use case

#### Scenario: Valid values documentation
- **WHEN** user needs to know valid filter values
- **THEN** they find chain IDs can be looked up with `listChains` tool
- **AND** they find complete lists of operation_types and position_types
- **AND** they find examples of fungible_ids format

#### Scenario: Filter validation examples
- **WHEN** user reads filter documentation
- **THEN** they find at least 15 concrete filter examples
- **AND** examples cover all major filter parameters
- **AND** examples show both single and combined filters

