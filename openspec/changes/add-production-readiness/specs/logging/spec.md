## ADDED Requirements

### Requirement: Structured Logging
The system SHALL implement structured logging with configurable levels and formats.

#### Scenario: Logger initialization
- **WHEN** server starts
- **THEN** logging is configured based on config settings
- **AND** log level is set (DEBUG, INFO, WARN, ERROR)
- **AND** log format is applied (text or JSON)

#### Scenario: JSON format
- **WHEN** logging.format is set to "json"
- **THEN** all logs are emitted as JSON objects
- **AND** each log includes timestamp, level, message, and context
- **AND** structured data is preserved

#### Scenario: Text format
- **WHEN** logging.format is set to "text"
- **THEN** logs are human-readable text
- **AND** format includes timestamp, level, and message
- **AND** suitable for development/debugging

### Requirement: Request Logging
The system SHALL log all API requests and responses.

#### Scenario: Outgoing request log
- **WHEN** HTTP request is sent to Zerion API
- **THEN** request is logged at INFO level
- **AND** log includes method, URL, and headers (excluding auth)
- **AND** request body is logged at DEBUG level

#### Scenario: API response log
- **WHEN** response is received from Zerion API
- **THEN** response is logged at INFO level
- **AND** log includes status code and duration
- **AND** response body is logged at DEBUG level

#### Scenario: Failed request log
- **WHEN** API request fails
- **THEN** failure is logged at ERROR level
- **AND** log includes error type and message
- **AND** full context is logged at DEBUG level

### Requirement: Performance Logging
The system SHALL log performance metrics for operations.

#### Scenario: Operation timing
- **WHEN** any operation completes
- **THEN** duration is logged at DEBUG level
- **AND** log includes operation name
- **AND** slow operations (>1s) are logged at WARN level

#### Scenario: OpenAPI spec load timing
- **WHEN** OpenAPI spec is loaded
- **THEN** load duration is logged
- **AND** spec size is logged
- **AND** parse time is logged separately

### Requirement: Startup Logging
The system SHALL log detailed startup information.

#### Scenario: Configuration loaded
- **WHEN** configuration is successfully loaded
- **THEN** log configuration source (file path or defaults)
- **AND** log key settings (excluding secrets)
- **AND** log at INFO level

#### Scenario: Server ready
- **WHEN** MCP server is ready to accept requests
- **THEN** log "Server started successfully"
- **AND** log server name and version
- **AND** log available tools count

#### Scenario: Startup failure
- **WHEN** server fails to start
- **THEN** log failure reason at ERROR level
- **AND** log configuration state
- **AND** log suggested remediation

### Requirement: Security Logging
The system SHALL not log sensitive information.

#### Scenario: API key redaction
- **WHEN** logging headers or config
- **THEN** Authorization header is redacted
- **AND** api_key field shows only "***REDACTED***"
- **AND** no bearer tokens appear in logs

#### Scenario: Sensitive data filtering
- **WHEN** logging request/response bodies
- **THEN** sensitive fields are redacted
- **AND** wallet addresses are preserved (not sensitive)
- **AND** API keys and secrets are masked
