## ADDED Requirements

### Requirement: Configuration File Support
The system SHALL support loading configuration from YAML files.

#### Scenario: Load from config file
- **WHEN** config.yaml exists in current directory
- **THEN** configuration is loaded from file
- **AND** all settings are validated
- **AND** missing required fields raise ConfigError

#### Scenario: Default config path
- **WHEN** no config file path is specified
- **THEN** system checks for config.yaml in current directory
- **AND** falls back to hardcoded defaults if not found

#### Scenario: Custom config path
- **WHEN** CONFIG_PATH environment variable is set
- **THEN** configuration is loaded from specified path
- **AND** error is raised if file does not exist

### Requirement: Environment Variable Overrides
The system SHALL allow environment variables to override config file values.

#### Scenario: Override API key
- **WHEN** ZERION_API_KEY environment variable is set
- **THEN** it overrides api_key from config file
- **AND** takes precedence over all other sources

#### Scenario: Override base URL
- **WHEN** ZERION_BASE_URL environment variable is set
- **THEN** it overrides base_url from config file
- **AND** is used for HTTP client initialization

### Requirement: Configuration Validation
The system SHALL validate all configuration values on load.

#### Scenario: Valid configuration
- **WHEN** configuration is loaded
- **THEN** required fields (api_key, base_url) are present
- **AND** URLs are properly formatted
- **AND** no validation errors are raised

#### Scenario: Invalid configuration
- **WHEN** required field is missing
- **THEN** ConfigError is raised
- **AND** error message specifies which field is missing
- **AND** server does not start

### Requirement: Configuration Schema
The system SHALL support the following configuration structure:

```yaml
name: "Zerion API"
base_url: "https://api.zerion.io"
oas_url: "https://raw.githubusercontent.com/smart-mcp-proxy/zerion-mcp-server/main/zerion_mcp_server/openapi_zerion.yaml"
api_key: "${ZERION_API_KEY}"  # Environment variable substitution
logging:
  level: "INFO"
  format: "json"
```

#### Scenario: Full config parsing
- **WHEN** complete config.yaml is loaded
- **THEN** all fields are accessible via ConfigManager
- **AND** environment variable substitution is performed
- **AND** nested objects (logging) are properly parsed
