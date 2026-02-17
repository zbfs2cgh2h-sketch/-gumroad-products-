"""
Structured logging with human-readable console + JSON file output
Built by Jackson Studio
"""

import logging
import json
import sys
from datetime import datetime
from pathlib import Path


class JSONFormatter(logging.Formatter):
    """JSON formatter for machine-readable logs"""
    
    def format(self, record):
        log_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        
        # Add extra fields
        if hasattr(record, "extra"):
            log_data.update(record.extra)
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_data)


class HumanFormatter(logging.Formatter):
    """Human-readable formatter with colors"""
    
    COLORS = {
        "DEBUG": "\033[36m",    # Cyan
        "INFO": "\033[32m",     # Green
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",    # Red
        "CRITICAL": "\033[35m", # Magenta
        "RESET": "\033[0m",
    }
    
    def format(self, record):
        color = self.COLORS.get(record.levelname, self.COLORS["RESET"])
        reset = self.COLORS["RESET"]
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        base_msg = f"[{timestamp}] {color}{record.levelname}{reset} {record.getMessage()}"
        
        # Add extra fields as key=value
        if hasattr(record, "extra"):
            extras = " ".join(f"{k}={v}" for k, v in record.extra.items())
            base_msg += f" {extras}"
        
        return base_msg


def setup_logging(level="INFO", log_format="text", log_file=None):
    """Setup logging with console + optional file output"""
    
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    
    # Clear existing handlers
    root_logger.handlers = []
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    if log_format == "json":
        console_handler.setFormatter(JSONFormatter())
    else:
        console_handler.setFormatter(HumanFormatter())
    root_logger.addHandler(console_handler)
    
    # File handler (if specified)
    if log_file:
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(JSONFormatter())
        root_logger.addHandler(file_handler)


def get_logger(name):
    """Get a logger instance with extra field support"""
    
    logger = logging.getLogger(name)
    
    # Monkey-patch to support extra dict
    original_log = logger._log
    
    def _log_with_extra(level, msg, args, exc_info=None, extra=None, **kwargs):
        if extra:
            # Store extra in LogRecord
            kwargs["extra"] = {"extra": extra}
        original_log(level, msg, args, exc_info=exc_info, **kwargs)
    
    logger._log = _log_with_extra
    return logger
