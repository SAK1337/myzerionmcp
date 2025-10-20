## ADDED Requirements

### Requirement: Custom Exception Classes
The system SHALL define custom exception classes for different error categories.

#### Scenario: Exception hierarchy
- **WHEN** error conditions occur
- **THEN** appropriate custom exception is raised
- **AND** exception inherits from base ZerionMCPError
- **AND** exception includes descriptive message and context

#### Scenario: Available exceptions
- **WHEN** system needs to raise errors
- **THEN** following exceptions are available:
  - ConfigError - configuration issues
  - APIError - Zerion API failures
  - ValidationError - data validation failures
  - NetworkError - connectivity issues

### Requirement: Network Error Handling
The system SHALL handle network failures gracefully.

#### Scenario: Connection timeout
- **WHEN** HTTP request times out
- **THEN** NetworkError is raised with timeout details
- **AND** error message includes endpoint and duration
- **AND** request is not retried automatically

#### Scenario: DNS resolution failure
- **WHEN** hostname cannot be resolved
- **THEN** NetworkError is raised with DNS error details
- **AND** user-friendly message suggests checking connectivity

#### Scenario: Connection refused
- **WHEN** connection is refused by server
- **THEN** NetworkError is raised with server details
- **AND** message suggests checking server status

### Requirement: API Error Handling
The system SHALL handle Zerion API errors appropriately.

#### Scenario: 401 Unauthorized
- **WHEN** API returns 401 status
- **THEN** APIError is raised with authentication context
- **AND** message suggests checking ZERION_API_KEY
- **AND** response body is logged for debugging

#### Scenario: 429 Rate Limit
- **WHEN** API returns 429 status
- **THEN** APIError is raised with rate limit details
- **AND** message includes retry-after header if present
- **AND** suggests waiting before retrying

#### Scenario: 500 Server Error
- **WHEN** API returns 5xx status
- **THEN** APIError is raised with server error context
- **AND** message indicates temporary issue
- **AND** suggests retrying later

#### Scenario: Invalid JSON response
- **WHEN** API returns malformed JSON
- **THEN** ValidationError is raised
- **AND** raw response is logged
- **AND** message indicates parsing failure

### Requirement: OpenAPI Spec Loading Errors
The system SHALL handle OpenAPI specification loading failures.

#### Scenario: Spec URL unreachable
- **WHEN** OpenAPI spec cannot be downloaded
- **THEN** NetworkError is raised
- **AND** error message includes spec URL
- **AND** suggests checking internet connectivity

#### Scenario: Invalid YAML
- **WHEN** OpenAPI spec contains invalid YAML
- **THEN** ValidationError is raised
- **AND** YAML parsing error details are included
- **AND** message suggests checking spec file

#### Scenario: Invalid OpenAPI schema
- **WHEN** OpenAPI spec fails FastMCP validation
- **THEN** ValidationError is raised
- **AND** validation errors are logged
- **AND** message indicates spec incompatibility

### Requirement: User-Friendly Error Messages
The system SHALL provide clear, actionable error messages.

#### Scenario: Error message format
- **WHEN** any error occurs
- **THEN** error message includes:
  - Clear description of what went wrong
  - Context (which operation, what inputs)
  - Actionable troubleshooting steps
  - Relevant documentation links

#### Scenario: Error logging
- **WHEN** error is raised
- **THEN** full stack trace is logged at DEBUG level
- **AND** error summary is logged at ERROR level
- **AND** user sees simplified error message
