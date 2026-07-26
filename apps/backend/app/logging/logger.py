"""
AegisSOC Central Logging Framework

Purpose:
Provides centralized logging for:
- Application events
- API events
- Security events
- Audit events

Security:
- No passwords or secrets should be logged.
- Sensitive information must be masked before logging.
"""

import logging
import os

from logging.handlers import RotatingFileHandler


BASE_LOG_PATH = "logs"


def create_logger(
    name: str,
    log_file: str,
    level: str = "INFO"
):
    """
    Creates a secure rotating logger.

    Args:
        name:
            Logger name

        log_file:
            Log file name

        level:
            Logging level

    Returns:
        Configured logger object
    """

    logger = logging.getLogger(name)

    logger.setLevel(level)

    # Avoid duplicate handlers
    if logger.handlers:
        return logger


    formatter = logging.Formatter(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(name)s | "
        "%(message)s"
    )


    os.makedirs(
        BASE_LOG_PATH,
        exist_ok=True
    )


    file_handler = RotatingFileHandler(
        filename=f"{BASE_LOG_PATH}/{log_file}",
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8"
    )


    file_handler.setFormatter(formatter)


    logger.addHandler(
        file_handler
    )


    return logger



# Application logger
app_logger = create_logger(
    "AegisSOC",
    "aegissoc.log"
)


# API logger
api_logger = create_logger(
    "API",
    "api.log"
)


# Security logger
security_logger = create_logger(
    "Security",
    "security.log"
)


# Audit logger
audit_logger = create_logger(
    "Audit",
    "audit.log"
)