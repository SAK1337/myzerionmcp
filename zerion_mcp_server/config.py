#!/usr/bin/env python3
"""Configuration management for Zerion MCP Server."""

import os
import re
from pathlib import Path
from typing import Any, Dict, Optional
import yaml

from .errors import ConfigError


class ConfigManager:
    """Manages configuration loading from YAML files and environment variables."""
    
    DEFAULT_CONFIG = {
        "name": "Zerion API",
        "base_url": "https://api.zerion.io",
        "oas_url": "https://raw.githubusercontent.com/smart-mcp-proxy/zerion-mcp-server/main/zerion_mcp_server/openapi_zerion.yaml",
        "logging": {
            "level": "INFO",
            "format": "text"
        },
        "retry_policy": {
            "max_attempts": 5,
            "base_delay": 1,
            "max_delay": 60,
            "exponential_base": 2
        },
        "wallet_indexing": {
            "retry_delay": 3,
            "max_retries": 3,
            "auto_retry": True
        }
    }
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration manager.
        
        Args:
            config_path: Path to YAML config file. If None, uses default search paths.
        """
        self._config: Dict[str, Any] = {}
        self._load_config(config_path)
        self._apply_env_overrides()
        self._validate()
    
    def _load_config(self, config_path: Optional[str] = None) -> None:
        """Load configuration from file or use defaults.
        
        Args:
            config_path: Path to YAML config file.
        """
        # Start with defaults
        self._config = self.DEFAULT_CONFIG.copy()
        
        # Determine config file path
        if config_path:
            path = Path(config_path)
        else:
            # Check CONFIG_PATH env var
            env_path = os.getenv("CONFIG_PATH")
            if env_path:
                path = Path(env_path)
            else:
                # Default to config.yaml in current directory
                path = Path("config.yaml")
        
        # Load from file if it exists
        if path.exists():
            try:
                with open(path, "r", encoding="utf-8") as f:
                    file_config = yaml.safe_load(f) or {}
                    # Merge with defaults (file values override defaults)
                    self._config.update(file_config)
            except yaml.YAMLError as e:
                raise ConfigError(f"Invalid YAML in config file {path}: {e}")
            except Exception as e:
                raise ConfigError(f"Failed to load config file {path}: {e}")
        elif config_path or os.getenv("CONFIG_PATH"):
            # If path was explicitly provided but doesn't exist, raise error
            raise ConfigError(f"Config file not found: {path}")
    
    def _apply_env_overrides(self) -> None:
        """Apply environment variable overrides to configuration."""
        # Override API key
        api_key = os.getenv("ZERION_API_KEY")
        if api_key:
            self._config["api_key"] = api_key
        
        # Override base URL
        base_url = os.getenv("ZERION_BASE_URL")
        if base_url:
            self._config["base_url"] = base_url
        
        # Override OAS URL
        oas_url = os.getenv("ZERION_OAS_URL")
        if oas_url:
            self._config["oas_url"] = oas_url
        
        # Override log level
        log_level = os.getenv("LOG_LEVEL")
        if log_level:
            self._config.setdefault("logging", {})["level"] = log_level
        
        # Override log format
        log_format = os.getenv("LOG_FORMAT")
        if log_format:
            self._config.setdefault("logging", {})["format"] = log_format
        
        # Substitute environment variables in config values
        self._substitute_env_vars(self._config)
    
    def _substitute_env_vars(self, obj: Any) -> None:
        """Recursively substitute ${VAR} patterns with environment variables.
        
        Args:
            obj: Configuration object (dict, list, or scalar).
        """
        if isinstance(obj, dict):
            for key, value in obj.items():
                if isinstance(value, str):
                    obj[key] = self._expand_env_var(value)
                elif isinstance(value, (dict, list)):
                    self._substitute_env_vars(value)
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                if isinstance(item, str):
                    obj[i] = self._expand_env_var(item)
                elif isinstance(item, (dict, list)):
                    self._substitute_env_vars(item)
    
    def _expand_env_var(self, value: str) -> str:
        """Expand ${VAR} or $VAR patterns in string.
        
        Args:
            value: String potentially containing env var references.
            
        Returns:
            String with environment variables expanded.
        """
        # Pattern matches ${VAR} or $VAR
        pattern = r'\$\{([^}]+)\}|\$([A-Za-z_][A-Za-z0-9_]*)'
        
        def replace(match):
            var_name = match.group(1) or match.group(2)
            return os.getenv(var_name, match.group(0))
        
        return re.sub(pattern, replace, value)
    
    def _validate(self) -> None:
        """Validate required configuration fields."""
        # Check for API key
        if "api_key" not in self._config:
            raise ConfigError(
                "Missing required configuration: api_key\n"
                "Set ZERION_API_KEY environment variable or add 'api_key' to config.yaml\n"
                "Example: export ZERION_API_KEY='Bearer your-api-key-here'"
            )
        
        # Check for base URL
        if not self._config.get("base_url"):
            raise ConfigError("Missing required configuration: base_url")
        
        # Validate base URL format
        base_url = self._config["base_url"]
        if not base_url.startswith(("http://", "https://")):
            raise ConfigError(f"Invalid base_url format: {base_url} (must start with http:// or https://)")
        
        # Check for OAS URL
        if not self._config.get("oas_url"):
            raise ConfigError("Missing required configuration: oas_url")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key.
        
        Args:
            key: Configuration key (supports dot notation, e.g., 'logging.level').
            default: Default value if key not found.
            
        Returns:
            Configuration value or default.
        """
        keys = key.split(".")
        value = self._config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        
        return value
    
    @property
    def name(self) -> str:
        """Get server name."""
        return self._config.get("name", "Zerion API")
    
    @property
    def base_url(self) -> str:
        """Get Zerion API base URL."""
        return self._config["base_url"]
    
    @property
    def oas_url(self) -> str:
        """Get OpenAPI specification URL."""
        return self._config["oas_url"]
    
    @property
    def api_key(self) -> str:
        """Get API key."""
        return self._config["api_key"]
    
    @property
    def log_level(self) -> str:
        """Get logging level."""
        return self._config.get("logging", {}).get("level", "INFO")
    
    @property
    def log_format(self) -> str:
        """Get logging format."""
        return self._config.get("logging", {}).get("format", "text")

    @property
    def retry_config(self) -> Dict[str, Any]:
        """Get retry policy configuration."""
        return self._config.get("retry_policy", {
            "max_attempts": 5,
            "base_delay": 1,
            "max_delay": 60,
            "exponential_base": 2
        })

    @property
    def indexing_config(self) -> Dict[str, Any]:
        """Get wallet indexing configuration."""
        return self._config.get("wallet_indexing", {
            "retry_delay": 3,
            "max_retries": 3,
            "auto_retry": True
        })

    @property
    def pagination_config(self) -> Dict[str, Any]:
        """Get pagination configuration."""
        return self._config.get("pagination", {
            "default_page_size": 100,
            "max_auto_pages": 50
        })

    def to_dict(self, redact_secrets: bool = True) -> Dict[str, Any]:
        """Export configuration as dictionary.
        
        Args:
            redact_secrets: Whether to redact sensitive values.
            
        Returns:
            Configuration dictionary.
        """
        config = self._config.copy()
        
        if redact_secrets and "api_key" in config:
            config["api_key"] = "***REDACTED***"
        
        return config
