"""
DevScope - Structured Logging Module
Configures application-wide logging formats and destination handlers.
"""

import logging
import sys
from config import LOG_FORMAT, LOG_LEVEL

def get_logger(name: str) -> logging.Logger:
    """Returns a configured logger instance for the given module name."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(getattr(logging, LOG_LEVEL.upper(), logging.INFO))
        
        # Console handler
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(LOG_FORMAT)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
    return logger
