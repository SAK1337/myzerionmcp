## Why
The Zerion MCP server currently has functional core capabilities but lacks production-grade features needed for reliability, maintainability, and operability. There is no baseline specification documenting current behavior, no error handling, minimal logging, no tests, hardcoded configuration, and sparse documentation. These gaps create risk for production use and hinder future development.

## What Changes
- **Document current state**: Create baseline specifications for existing MCP server functionality
- **Error handling**: Add comprehensive error handling for network failures, API errors, and validation
- **Logging**: Implement structured logging for observability and debugging
- **Testing infrastructure**: Set up pytest with unit and integration tests
- **Configuration system**: Replace hardcoded values with flexible YAML/env-based configuration
- **Enhanced documentation**: Comprehensive README, usage examples, and setup guide

## Impact
- **Affected specs**: 
  - `mcp-server` (new baseline + improvements)
  - `error-handling` (new)
  - `logging` (new)  
  - `testing` (new)
  - `configuration` (new)
  - `documentation` (new)

- **Affected code**:
  - `zerion_mcp_server/__init__.py` - main server implementation
  - New: `zerion_mcp_server/config.py` - configuration management
  - New: `zerion_mcp_server/logger.py` - logging setup
  - New: `tests/` - test suite
  - `README.md` - enhanced documentation
  - `pyproject.toml` - add test dependencies

- **Breaking changes**: None - purely additive improvements
- **Migration**: Existing usage continues to work; new features are opt-in
