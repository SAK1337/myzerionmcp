# testnet-support Specification

## Purpose
TBD - created by archiving change validate-feature-parity. Update Purpose after archive.
## Requirements
### Requirement: X-Env Header Validation
The MCP server SHALL validate that the `X-Env` header parameter works correctly for accessing testnet data and document which endpoints support testnets.

#### Scenario: Testnet positions query
- **WHEN** user calls `listWalletPositions` with `X-Env=testnet` header
- **THEN** testnet position data is returned (if testnet API access is available)
- **OR** appropriate error message indicates testnet access requirements
- **AND** mainnet data is NOT returned

#### Scenario: Testnet portfolio query
- **WHEN** user calls `getWalletPortfolio` with `X-Env=testnet` header
- **THEN** testnet portfolio data is returned
- **AND** testnet chains (Sepolia, Monad Testnet, etc.) are included

#### Scenario: Testnet transaction history
- **WHEN** user calls `listWalletTransactions` with `X-Env=testnet` header
- **THEN** testnet transactions are returned
- **AND** mainnet transactions are NOT included

#### Scenario: Endpoint testnet compatibility
- **WHEN** user checks OpenAPI spec for testnet support
- **THEN** they can identify which endpoints support X-Env header
- **AND** documentation lists all testnet-compatible endpoints

---

### Requirement: Testnet Documentation
The README SHALL document testnet support via X-Env header with examples and requirements.

#### Scenario: Testnet section in README
- **WHEN** user reads testnet documentation
- **THEN** they find explanation of X-Env header
- **AND** they find list of testnet-supported endpoints
- **AND** they find requirements for testnet API access

#### Scenario: Testnet usage examples
- **WHEN** user reads testnet documentation
- **THEN** they find at least 3 concrete examples using X-Env header
- **AND** examples cover positions, portfolio, and transactions
- **AND** examples explain expected testnet behavior

#### Scenario: Testnet API key guidance
- **WHEN** user reads testnet documentation
- **THEN** they find information about obtaining testnet API credentials
- **AND** they understand testnet may require separate API key
- **AND** they find link to Zerion testnet documentation

---

### Requirement: Testnet Development Workflow Documentation
The README SHALL document how to use testnets for development before mainnet deployment.

#### Scenario: Development workflow guidance
- **WHEN** developer reads testnet documentation
- **THEN** they find recommended workflow for testnet-first development
- **AND** they understand benefits of testing on testnets
- **AND** they find examples of testing wallet creation before mainnet

#### Scenario: Testnet chain listing
- **WHEN** user reads testnet documentation
- **THEN** they find list of supported testnet chains (Sepolia, Monad Testnet, etc.)
- **AND** they can use `listChains` tool with X-Env header to see all testnets
- **AND** documentation explains how to verify testnet chain IDs

#### Scenario: Testnet limitations documentation
- **WHEN** user reads testnet documentation
- **THEN** they find any limitations of testnet data vs. mainnet
- **AND** they understand that not all features may be available on testnets
- **AND** they find guidance for what to test on testnets

---

### Requirement: Testnet Parameter Testing
The MCP server SHALL include tests validating X-Env header parameter behavior.

#### Scenario: X-Env header test (if testnet credentials available)
- **WHEN** validation test runs with testnet API credentials
- **THEN** test confirms X-Env header passes through to API
- **AND** test verifies testnet data is returned
- **AND** test validates response structure matches mainnet

#### Scenario: X-Env header test (without testnet credentials)
- **WHEN** validation test runs without testnet API credentials
- **THEN** test documents that X-Env parameter exists in schema
- **AND** test validates parameter is accepted by MCP tools
- **AND** test skips actual API call with clear message

#### Scenario: Testnet endpoint coverage test
- **WHEN** validation test analyzes OpenAPI spec
- **THEN** test identifies all endpoints with X-Env header
- **AND** test validates documentation matches spec
- **AND** test reports any discrepancies

