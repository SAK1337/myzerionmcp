#!/usr/bin/env python3
"""Tests for configuration management."""

import pytest
import yaml
from pathlib import Path
from zerion_mcp_server.config import ConfigManager
from zerion_mcp_server.errors import ConfigError


class TestConfigManager:
    """Test ConfigManager class."""
    
    def test_load_from_file(self, config_file: Path, sample_config):
        """Test loading configuration from YAML file."""
        config = ConfigManager(str(config_file))
        
        assert config.name == sample_config["name"]
        assert config.base_url == sample_config["base_url"]
        assert config.oas_url == sample_config["oas_url"]
        assert config.api_key == sample_config["api_key"]
        assert config.log_level == sample_config["logging"]["level"]
        assert config.log_format == sample_config["logging"]["format"]
    
    def test_default_config(self, clear_env_vars, monkeypatch):
        """Test default configuration when no file exists."""
        monkeypatch.setenv("ZERION_API_KEY", "Bearer test-key")
        
        config = ConfigManager()
        
        assert config.name == "Zerion API"
        assert config.base_url == "https://api.zerion.io"
        assert config.api_key == "Bearer test-key"
        assert config.log_level == "INFO"
        assert config.log_format == "text"
    
    def test_env_override_api_key(self, config_file: Path, monkeypatch):
        """Test environment variable override for API key."""
        env_key = "Bearer env-override-key"
        monkeypatch.setenv("ZERION_API_KEY", env_key)
        
        config = ConfigManager(str(config_file))
        
        assert config.api_key == env_key
    
    def test_env_override_base_url(self, config_file: Path, monkeypatch):
        """Test environment variable override for base URL."""
        env_url = "https://custom.api.example.com"
        monkeypatch.setenv("ZERION_BASE_URL", env_url)
        monkeypatch.setenv("ZERION_API_KEY", "Bearer test")
        
        config = ConfigManager(str(config_file))
        
        assert config.base_url == env_url
    
    def test_env_override_log_level(self, config_file: Path, monkeypatch):
        """Test environment variable override for log level."""
        monkeypatch.setenv("LOG_LEVEL", "ERROR")
        monkeypatch.setenv("ZERION_API_KEY", "Bearer test")
        
        config = ConfigManager(str(config_file))
        
        assert config.log_level == "ERROR"
    
    def test_missing_api_key(self, tmp_path: Path, clear_env_vars):
        """Test error when API key is missing."""
        config_path = tmp_path / "config.yaml"
        with open(config_path, "w") as f:
            yaml.dump({"base_url": "https://api.example.com"}, f)
        
        with pytest.raises(ConfigError) as exc_info:
            ConfigManager(str(config_path))
        
        assert "api_key" in str(exc_info.value).lower()
    
    def test_missing_base_url(self, tmp_path: Path, monkeypatch, clear_env_vars):
        """Test error when base URL is missing."""
        monkeypatch.setenv("ZERION_API_KEY", "Bearer test")
        
        config_path = tmp_path / "config.yaml"
        with open(config_path, "w") as f:
            yaml.dump({"base_url": ""}, f)
        
        with pytest.raises(ConfigError) as exc_info:
            ConfigManager(str(config_path))
        
        assert "base_url" in str(exc_info.value).lower()
    
    def test_invalid_base_url_format(self, tmp_path: Path, monkeypatch, clear_env_vars):
        """Test error when base URL has invalid format."""
        monkeypatch.setenv("ZERION_API_KEY", "Bearer test")
        
        config_path = tmp_path / "config.yaml"
        with open(config_path, "w") as f:
            yaml.dump({
                "base_url": "not-a-url",
                "oas_url": "https://example.com/spec.yaml"
            }, f)
        
        with pytest.raises(ConfigError) as exc_info:
            ConfigManager(str(config_path))
        
        assert "base_url" in str(exc_info.value).lower()
    
    def test_invalid_yaml(self, tmp_path: Path):
        """Test error when YAML is invalid."""
        config_path = tmp_path / "config.yaml"
        with open(config_path, "w") as f:
            f.write("invalid: yaml: content:\n  - bad")
        
        with pytest.raises(ConfigError) as exc_info:
            ConfigManager(str(config_path))
        
        assert "yaml" in str(exc_info.value).lower()
    
    def test_nonexistent_explicit_path(self, clear_env_vars):
        """Test error when explicitly provided path doesn't exist."""
        with pytest.raises(ConfigError) as exc_info:
            ConfigManager("/nonexistent/path/config.yaml")
        
        assert "not found" in str(exc_info.value).lower()
    
    def test_env_var_substitution(self, tmp_path: Path, monkeypatch, clear_env_vars):
        """Test environment variable substitution in config values."""
        monkeypatch.setenv("MY_API_KEY", "Bearer substituted-key")
        
        config_path = tmp_path / "config.yaml"
        with open(config_path, "w") as f:
            yaml.dump({
                "base_url": "https://api.zerion.io",
                "oas_url": "https://example.com/spec.yaml",
                "api_key": "${MY_API_KEY}"
            }, f)
        
        config = ConfigManager(str(config_path))
        
        assert config.api_key == "Bearer substituted-key"
    
    def test_get_method(self, config_file: Path):
        """Test get method for accessing config values."""
        config = ConfigManager(str(config_file))
        
        assert config.get("name") == "Test Zerion API"
        assert config.get("logging.level") == "DEBUG"
        assert config.get("logging.format") == "text"
        assert config.get("nonexistent", "default") == "default"
    
    def test_to_dict_with_redaction(self, config_file: Path):
        """Test exporting config as dict with secret redaction."""
        config = ConfigManager(str(config_file))
        
        config_dict = config.to_dict(redact_secrets=True)
        
        assert config_dict["api_key"] == "***REDACTED***"
        assert config_dict["base_url"] == "https://api.zerion.io"
    
    def test_to_dict_without_redaction(self, config_file: Path):
        """Test exporting config as dict without redaction."""
        config = ConfigManager(str(config_file))
        
        config_dict = config.to_dict(redact_secrets=False)
        
        assert config_dict["api_key"] == "Bearer test-api-key-123"
