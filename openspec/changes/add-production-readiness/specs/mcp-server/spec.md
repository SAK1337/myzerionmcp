## ADDED Requirements

### Requirement: MCP Server Initialization
The system SHALL initialize a FastMCP server that exposes Zerion API operations as MCP tools.

#### Scenario: Successful initialization
- **WHEN** the server starts with valid configuration
- **THEN** FastMCP server is created from OpenAPI spec
- **AND** HTTP client is configured with base URL and headers
- **AND** server is ready to accept MCP requests

#### Scenario: Missing API key
- **WHEN** ZERION_API_KEY environment variable is not set
- **THEN** server SHALL print error message with setup instructions
- **AND** server SHALL exit gracefully without starting

### Requirement: OpenAPI Specification Loading
The system SHALL fetch and parse the Zerion OpenAPI specification at runtime.

#### Scenario: Successful spec loading
- **WHEN** server initializes
- **THEN** OpenAPI spec is fetched from configured URL
- **AND** YAML content is parsed into Python dictionary
- **AND** spec is validated by FastMCP

#### Scenario: Network failure during spec load
- **WHEN** OpenAPI spec URL is unreachable
- **THEN** server SHALL log the error with URL details
- **AND** server SHALL exit with clear error message

### Requirement: HTTP Client Configuration
The system SHALL configure an async HTTP client with proper authentication headers.

#### Scenario: Client setup with API key
- **WHEN** server initializes with valid ZERION_API_KEY
- **THEN** httpx.AsyncClient is created
- **AND** Authorization header is set to API key value
- **AND** base_url is set to Zerion API endpoint

### Requirement: MCP Tool Generation
The system SHALL auto-generate MCP tools from OpenAPI operations.

#### Scenario: Route mapping
- **WHEN** FastMCP processes OpenAPI spec
- **THEN** each API endpoint becomes an MCP tool
- **AND** tools are registered with MCPType.TOOL
- **AND** parameter schemas match OpenAPI definitions

### Requirement: Server Execution
The system SHALL run the MCP server and handle requests.

#### Scenario: Server running
- **WHEN** mcp.run() is called
- **THEN** server listens for MCP protocol messages
- **AND** tool invocations are routed to Zerion API
- **AND** responses are returned via MCP protocol
