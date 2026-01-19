"""Structured logging with automatic PII redaction."""
import logging
import json
import re
from typing import Any, Dict, Optional
from datetime import datetime
from pathlib import Path


class PIIRedactor:
    """Redact PII from log messages."""
    
    PATTERNS = {
        'password': re.compile(r'password[\"\']?\s*[:=]\s*[\"\'](.*?)[\"\']', re.IGNORECASE),
        'api_key': re.compile(r'api[_-]?key[\"\']?\s*[:=]\s*[\"\'](.*?)[\"\']', re.IGNORECASE),
        'token': re.compile(r'token[\"\']?\s*[:=]\s*[\"\'](.*?)[\"\']', re.IGNORECASE),
        'secret': re.compile(r'secret[\"\']?\s*[:=]\s*[\"\'](.*?)[\"\']', re.IGNORECASE),
        'credentials': re.compile(r'credentials[\"\']?\s*[:=]\s*[\"\'](.*?)[\"\']', re.IGNORECASE),
        'ssn': re.compile(r'\b\d{3}-\d{2}-\d{4}\b'),
        'credit_card': re.compile(r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b'),
    }
    
    @classmethod
    def redact(cls, data: Any) -> Any:
        """Redact PII from data."""
        if isinstance(data, dict):
            return {k: cls.redact(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [cls.redact(item) for item in data]
        elif isinstance(data, str):
            result = data
            for pattern in cls.PATTERNS.values():
                result = pattern.sub('[REDACTED]', result)
            return result
        return data


class JSONFormatter(logging.Formatter):
    """JSON log formatter with PII redaction."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.redactor = PIIRedactor()
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
        }
        
        # Add extra data if present
        if hasattr(record, 'data'):
            log_data['data'] = self.redactor.redact(record.data)
        
        # Add request context if present
        if hasattr(record, 'request_id'):
            log_data['request_id'] = record.request_id
        if hasattr(record, 'agent_id'):
            log_data['agent_id'] = record.agent_id
        
        # Add exception info if present
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
        
        return json.dumps(log_data)


def setup_logger(name: str = "policy-reader") -> logging.Logger:
    """Setup structured logger with PII redaction."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Create logs directory
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(JSONFormatter())
    logger.addHandler(console_handler)
    
    # File handler
    file_handler = logging.FileHandler(logs_dir / "app.log")
    file_handler.setFormatter(JSONFormatter())
    logger.addHandler(file_handler)
    
    return logger


# Global logger instance
logger = setup_logger()


def log_audit(event: str, **kwargs):
    """Log audit event."""
    logger.info(f"AUDIT: {event}", extra={'data': kwargs})


def log_metrics(metric_name: str, value: float, **labels):
    """Log metrics."""
    logger.info(f"METRIC: {metric_name}={value}", extra={'data': labels})


def set_request_context(request_id: str, agent_id: str):
    """Set request context for logging."""
    # This would be implemented with contextvars in production
    pass
