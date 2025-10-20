# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Configuration System**: YAML-based configuration with environment variable overrides
  - ConfigManager class for flexible configuration loading
  - Support for config.yaml files with ${VAR} substitution
  - Environment variables: ZERION_API_KEY, ZERION_BASE_URL, LOG_LEVEL, etc.
  - Example configuration file (config.example.yaml)
  
- **Logging Infrastructure**: Structured logging with multiple formats
  - JSON and text log formats
  - Configurable log levels (DEBUG, INFO, WARN, ERROR)
  - Automatic sensitive data redaction (API keys, Bearer tokens)
  - Request/response logging with timing metrics
  - Performance logging for operations
  
- **Error Handling**: Comprehensive custom exception hierarchy
  - ConfigError for configuration issues
  - NetworkError for connectivity problems
  - APIError for Zerion API failures with status code handling
  - ValidationError for data validation issues
  - Detailed error contexts and troubleshooting hints
  
- **Testing Infrastructure**: Full test suite with pytest
  - Unit tests for configuration (test_config.py)
  - Unit tests for error handling (test_errors.py)
  - Integration tests for server flow (test_integration.py)
  - Test fixtures and mocks (conftest.py)
  - Coverage reporting configuration
  - Development dependencies in pyproject.toml
  
- **Documentation**: Comprehensive project documentation
  - Detailed README with installation, configuration, and usage
  - Troubleshooting guide with common issues and solutions
  - Architecture diagram
  - Contributing guidelines
  - This CHANGELOG

### Changed
- **Server Initialization**: Enhanced error handling during startup
  - Better error messages for missing API keys
  - Detailed logging of initialization steps
  - Graceful handling of OpenAPI spec loading failures
  
- **HTTP Client**: Improved configuration
  - Configurable timeouts (30 seconds default)
  - Better exception handling for network errors
  - Status code validation with raise_for_status()

### Fixed
- None (initial production-ready release)

## [0.1.0] - Initial Release

### Added
- Basic MCP server functionality
- FastMCP integration with OpenAPI spec
- Zerion API proxy via MCP protocol
- httpx async HTTP client
- Basic package structure

[Unreleased]: https://github.com/SAK1337/myzerionmcp/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/SAK1337/myzerionmcp/releases/tag/v0.1.0
