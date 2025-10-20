#!/usr/bin/env python3
"""Structured logging setup for Zerion MCP Server."""

import logging
import json
import sys
from typing import Any, Dict
from datetime import datetime, UTC


class JSONFormatter(logging.Formatter):
    """Custom formatter that outputs logs as JSON."""
    
    SENSITIVE_FIELDS = {"authorization", "api_key", "token", "password", "secret"}
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON.
        
        Args:
            record: Log record to format.
            
        Returns:
            JSON string representation of log record.
        """
        log_data = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        
        # Add extra fields from record
        if hasattr(record, "extra"):
            log_data.update(self._redact_sensitive(record.extra))
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_data)
    
    def _redact_sensitive(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Redact sensitive fields from log data.
        
        Args:
            data: Dictionary potentially containing sensitive data.
            
        Returns:
            Dictionary with sensitive fields redacted.
        """
        redacted = {}
        for key, value in data.items():
            key_lower = key.lower()
            if any(sensitive in key_lower for sensitive in self.SENSITIVE_FIELDS):
                redacted[key] = "***REDACTED***"
            elif isinstance(value, dict):
                redacted[key] = self._redact_sensitive(value)
            else:
                redacted[key] = value
        return redacted


class TextFormatter(logging.Formatter):
    """Human-readable text formatter with sensitive data redaction."""
    
    SENSITIVE_FIELDS = {"authorization", "api_key", "token", "password", "secret"}
    
    def __init__(self):
        """Initialize text formatter."""
        super().__init__(
            fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as text with redaction.
        
        Args:
            record: Log record to format.
            
        Returns:
            Formatted text string.
        """
        # Redact sensitive data in message
        original_msg = record.msg
        if isinstance(original_msg, str):
            record.msg = self._redact_message(original_msg)
        
        result = super().format(record)
        record.msg = original_msg  # Restore original
        return result
    
    def _redact_message(self, message: str) -> str:
        """Redact sensitive patterns from message.
        
        Args:
            message: Log message.
            
        Returns:
            Message with sensitive data redacted.
        """
        # Simple Bearer token redaction
        import re
        message = re.sub(r'Bearer\s+[A-Za-z0-9_\-\.]+', 'Bearer ***REDACTED***', message)
        return message


def setup_logging(level: str = "INFO", format_type: str = "text") -> logging.Logger:
    """Set up logging for the application.
    
    Args:
        level: Log level (DEBUG, INFO, WARN, ERROR).
        format_type: Format type ('text' or 'json').
        
    Returns:
        Configured root logger.
    """
    # Convert level string to logging constant
    log_level = getattr(logging, level.upper(), logging.INFO)
    
    # Get root logger
    logger = logging.getLogger()
    logger.setLevel(log_level)
    
    # Remove existing handlers
    logger.handlers = []
    
    # Create console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level)
    
    # Set formatter
    if format_type.lower() == "json":
        formatter = JSONFormatter()
    else:
        formatter = TextFormatter()
    
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for a module.
    
    Args:
        name: Logger name (typically __name__).
        
    Returns:
        Logger instance.
    """
    return logging.getLogger(name)


class LogContext:
    """Context manager for adding extra fields to logs."""
    
    def __init__(self, logger: logging.Logger, **kwargs):
        """Initialize log context.
        
        Args:
            logger: Logger instance.
            **kwargs: Extra fields to add to log records.
        """
        self.logger = logger
        self.extra = kwargs
        self.old_factory = None
    
    def __enter__(self):
        """Enter context."""
        self.old_factory = logging.getLogRecordFactory()
        
        def record_factory(*args, **kwargs):
            record = self.old_factory(*args, **kwargs)
            record.extra = self.extra
            return record
        
        logging.setLogRecordFactory(record_factory)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context."""
        if self.old_factory:
            logging.setLogRecordFactory(self.old_factory)
