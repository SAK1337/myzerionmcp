# Pagination Handling Capability

## ADDED Requirements

### Requirement: Pagination Parameter Exposure
The MCP server SHALL expose `page[size]` and `page[after]` query parameters for endpoints that support pagination, enabling users to control result set size and fetch subsequent pages.

#### Scenario: Manual pagination with page size
- **WHEN** user calls `listWalletTransactions` with `page[size]=100`
- **THEN** the API returns up to 100 transactions
- **AND** includes `links.next` URL if more results exist

#### Scenario: Cursor-based pagination
- **WHEN** user calls `listWalletTransactions` with `page[after]` cursor from previous response
- **THEN** the API returns the next page of results starting after the cursor
- **AND** includes new `links.next` if more results exist

#### Scenario: Last page detection
- **WHEN** user fetches a page and `links.next` is not present in response
- **THEN** user knows they have reached the last page
- **AND** no further pagination is required

---

### Requirement: Auto-Pagination Helper
The MCP server SHALL provide an optional auto-pagination helper function that fetches all pages automatically until the result set is complete or a safety limit is reached.

#### Scenario: Fetch all transactions for active wallet
- **WHEN** user calls `fetch_all_pages(endpoint="listWalletTransactions", address="0x...", max_pages=50)`
- **THEN** the helper automatically fetches subsequent pages using `page[after]` cursors
- **AND** returns combined results from all pages
- **AND** stops at 50 pages or when no `links.next` exists

#### Scenario: Safety limit prevents quota exhaustion
- **WHEN** user calls `fetch_all_pages` with `max_pages=10`
- **THEN** the helper stops after 10 pages even if more results exist
- **AND** logs warning about incomplete results
- **AND** user can manually continue with last cursor

#### Scenario: Empty result set
- **WHEN** user calls `fetch_all_pages` for endpoint with no results
- **THEN** the helper returns empty list
- **AND** makes only one API request (first page)

---

### Requirement: Pagination Configuration
The MCP server SHALL allow configuration of pagination behavior including default page sizes and maximum auto-pagination depth.

#### Scenario: Configure default page size
- **WHEN** config.yaml sets `pagination.default_page_size: 50`
- **THEN** all pagination-enabled endpoints default to fetching 50 items per page
- **AND** users can override with explicit `page[size]` parameter

#### Scenario: Configure max auto-pagination pages
- **WHEN** config.yaml sets `pagination.max_auto_pages: 100`
- **THEN** `fetch_all_pages` stops after 100 pages
- **AND** prevents accidental quota exhaustion

---

### Requirement: Pagination Documentation
The README SHALL include comprehensive pagination guidance with examples for both manual and automatic pagination workflows.

#### Scenario: Manual pagination example
- **WHEN** user reads pagination documentation
- **THEN** they find example showing how to use `page[size]` and `page[after]`
- **AND** example demonstrates extracting `links.next` from response

#### Scenario: Auto-pagination example
- **WHEN** user reads pagination documentation
- **THEN** they find example using `fetch_all_pages` helper
- **AND** example shows quota impact warning

#### Scenario: Pagination best practices
- **WHEN** user reads pagination documentation
- **THEN** they find guidance on:
  - Choosing appropriate page sizes
  - Quota impact of fetching many pages
  - When to use manual vs auto-pagination
  - How to handle large result sets efficiently
