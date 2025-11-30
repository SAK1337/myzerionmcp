# Feature Parity Validation Tasks

## 1. Parameter Discovery & Analysis

- [ ] 1.1 List all filter parameters from OpenAPI spec by endpoint
- [ ] 1.2 List all endpoints that support X-Env header
- [ ] 1.3 List all endpoints that support currency parameter
- [ ] 1.4 Create parameter matrix (parameter → endpoints → schema type)
- [ ] 1.5 Identify which parameters are most critical for documentation

## 2. Filter Parameter Validation

- [ ] 2.1 Test `filter[chain_ids]` on listWalletPositions
- [ ] 2.2 Test `filter[chain_ids]` on listWalletTransactions
- [ ] 2.3 Test `filter[positions]=only_complex` on listWalletPositions
- [ ] 2.4 Test `filter[trash]=only_non_trash` on listWalletTransactions
- [ ] 2.5 Test `filter[operation_types]` on listWalletTransactions
- [ ] 2.6 Test `filter[position_types]` on listWalletPositions
- [ ] 2.7 Test `filter[fungible_ids]` on positions and transactions
- [ ] 2.8 Test filter combinations (chain + trash + operation_types)
- [ ] 2.9 Document actual behavior vs. expected for each filter

## 3. X-Env Testnet Header Validation

- [ ] 3.1 Check if testnet API credentials are available
- [ ] 3.2 Test X-Env header on listWalletPositions (if creds available)
- [ ] 3.3 Test X-Env header on getWalletPortfolio (if creds available)
- [ ] 3.4 Test X-Env header on listWalletTransactions (if creds available)
- [ ] 3.5 Document X-Env header usage regardless of validation status
- [ ] 3.6 Add note about testnet API key requirement

## 4. Currency Parameter Validation

- [ ] 4.1 Test currency=usd on getWalletPortfolio
- [ ] 4.2 Test currency=eth on getWalletPortfolio
- [ ] 4.3 Test currency=eur on getWalletPortfolio
- [ ] 4.4 Test currency=btc on getWalletPortfolio
- [ ] 4.5 Test currency parameter on listWalletPositions
- [ ] 4.6 Verify currency affects price fields in responses
- [ ] 4.7 Document which endpoints support currency parameter

## 5. Documentation Updates

- [ ] 5.1 Add "Filter Parameters Reference" table to README
- [ ] 5.2 Add 5+ examples for filter[chain_ids]
- [ ] 5.3 Add 3+ examples for filter[positions]=only_complex
- [ ] 5.4 Add 3+ examples for filter[trash]
- [ ] 5.5 Add 2+ examples for filter[operation_types]
- [ ] 5.6 Add 2+ examples for filter[position_types]
- [ ] 5.7 Add "Testnet Support" section with X-Env examples
- [ ] 5.8 Add "Multi-Currency Support" section with currency examples
- [ ] 5.9 Add "Common Filter Combinations" section with 5+ use cases
- [ ] 5.10 Update "Available Functions" section with filter parameter notes

## 6. Validation Test Suite

- [ ] 6.1 Create tests/test_filter_parameters.py
- [ ] 6.2 Write test for chain_ids filter validation
- [ ] 6.3 Write test for positions filter validation
- [ ] 6.4 Write test for trash filter validation
- [ ] 6.5 Write test for operation_types filter validation
- [ ] 6.6 Write test for currency parameter validation
- [ ] 6.7 Write test for filter combinations
- [ ] 6.8 Add test fixtures for common wallet addresses
- [ ] 6.9 Run validation test suite
- [ ] 6.10 Document test coverage in README

## 7. Feature Parity Matrix Update

- [ ] 7.1 Update GapAnalysis.md Section 3 with validation results
- [ ] 7.2 Change filter[chain_ids] status from ❓ to ✅ (if validated)
- [ ] 7.3 Change filter[trash] status from ❓ to ✅ (if validated)
- [ ] 7.4 Change filter[operation_types] status from ❓ to ✅ (if validated)
- [ ] 7.5 Change filter[positions] status from ❓ to ✅ (if validated)
- [ ] 7.6 Change filter[position_types] status from ❓ to ✅ (if validated)
- [ ] 7.7 Change X-Env testnet status from ❌ to ✅ or ⚠️ (documented)
- [ ] 7.8 Change currency status from ❓ to ✅ (if validated)
- [ ] 7.9 Add "Last Validated" timestamps
- [ ] 7.10 Create summary of validation findings

## 8. Quality Assurance

- [ ] 8.1 Run full test suite to ensure no regressions
- [ ] 8.2 Validate all README examples manually
- [ ] 8.3 Check that filter parameter names match OpenAPI spec exactly
- [ ] 8.4 Verify documentation examples use realistic wallet addresses
- [ ] 8.5 Test documentation examples with real API
- [ ] 8.6 Update CHANGELOG.md with validation work
- [ ] 8.7 Review all documentation for clarity and accuracy
- [ ] 8.8 Validate OpenSpec proposal with `openspec validate`
