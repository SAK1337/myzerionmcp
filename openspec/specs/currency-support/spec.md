# currency-support Specification

## Purpose
TBD - created by archiving change validate-feature-parity. Update Purpose after archive.
## Requirements
### Requirement: Currency Parameter Validation
The MCP server SHALL validate that the `currency` parameter works correctly for price conversions across supported currencies (USD, ETH, EUR, BTC).

#### Scenario: USD currency pricing
- **WHEN** user calls `getWalletPortfolio` with `currency=usd`
- **THEN** all price fields are returned in USD
- **AND** total_value uses USD denomination
- **AND** response validates currency parameter acceptance

#### Scenario: ETH currency pricing
- **WHEN** user calls `getWalletPortfolio` with `currency=eth`
- **THEN** all price fields are returned in ETH denomination
- **AND** prices reflect ETH-denominated values
- **AND** documentation explains ETH pricing use case

#### Scenario: EUR currency pricing
- **WHEN** user calls `getWalletPortfolio` with `currency=eur`
- **THEN** all price fields are returned in EUR
- **AND** EUR prices match expected exchange rates

#### Scenario: BTC currency pricing
- **WHEN** user calls `getWalletPortfolio` with `currency=btc`
- **THEN** all price fields are returned in BTC denomination
- **AND** BTC pricing use case is documented

#### Scenario: Default currency behavior
- **WHEN** user calls endpoints without currency parameter
- **THEN** default currency (USD) is used
- **AND** documentation clarifies default behavior

---

### Requirement: Currency Parameter Endpoint Coverage
The MCP server SHALL document which endpoints support the currency parameter and validate its behavior across those endpoints.

#### Scenario: Currency on portfolio endpoints
- **WHEN** user calls `getWalletPortfolio` with `currency=eth`
- **THEN** portfolio values are ETH-denominated
- **AND** documentation lists portfolio endpoint as currency-compatible

#### Scenario: Currency on positions endpoints
- **WHEN** user calls `listWalletPositions` with `currency=eur`
- **THEN** position values are EUR-denominated
- **AND** documentation lists positions endpoint as currency-compatible

#### Scenario: Currency on chart endpoints
- **WHEN** user calls `getWalletChart` with `currency=btc`
- **THEN** chart data points use BTC denomination
- **AND** documentation lists chart endpoint as currency-compatible

#### Scenario: Currency parameter unavailable endpoints
- **WHEN** user reads currency documentation
- **THEN** they find clear list of endpoints that DON'T support currency
- **AND** documentation explains why (e.g., transaction hashes don't have currency)

---

### Requirement: Multi-Currency Documentation
The README SHALL document multi-currency support with examples for each supported currency and guidance on when to use each.

#### Scenario: Currency parameter reference
- **WHEN** user reads multi-currency documentation
- **THEN** they find list of supported currencies (usd, eth, eur, btc)
- **AND** they find explanation of what currency parameter affects
- **AND** they find list of currency-compatible endpoints

#### Scenario: Currency usage examples
- **WHEN** user reads multi-currency documentation
- **THEN** they find at least one example per supported currency
- **AND** examples show realistic use cases
- **AND** examples demonstrate price field changes

#### Scenario: Currency use case guidance
- **WHEN** user reads multi-currency documentation
- **THEN** they find guidance on when to use USD (default, most common)
- **AND** they find ETH use case (DeFi analytics, ETH-native communities)
- **AND** they find EUR use case (European users, EU compliance)
- **AND** they find BTC use case (Bitcoin-maximalist perspectives)

---

### Requirement: Currency Parameter Testing
The MCP server SHALL include tests validating currency parameter behavior across supported currencies.

#### Scenario: USD currency test
- **WHEN** validation test runs for USD currency
- **THEN** test confirms USD pricing matches expected format
- **AND** test validates price fields are numeric
- **AND** test checks USD is default when parameter omitted

#### Scenario: ETH currency test
- **WHEN** validation test runs for ETH currency
- **THEN** test confirms ETH pricing is applied
- **AND** test validates ETH prices differ from USD prices
- **AND** test checks conversion accuracy (within margin)

#### Scenario: EUR and BTC currency tests
- **WHEN** validation tests run for EUR and BTC
- **THEN** tests confirm both currencies work
- **AND** tests validate price conversions are reasonable
- **AND** tests document any currency-specific behavior

#### Scenario: Invalid currency handling
- **WHEN** validation test uses invalid currency (e.g., "jpy")
- **THEN** test documents API error response
- **AND** test validates error message is helpful
- **AND** documentation includes valid currency list

