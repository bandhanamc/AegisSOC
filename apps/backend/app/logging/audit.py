"""
AegisSOC Audit Logging

Purpose:
Tracks security-sensitive activities.

Examples:
- User actions
- Configuration changes
- AI recommendations
- Analyst decisions
"""

from app.logging.logger import audit_logger



def log_audit_event(
    action: str,
    user: str,
    details: str
):
    """
    Writes audit events.

    Args:
        action:
            Action performed

        user:
            User/service responsible

        details:
            Event description
    """

    audit_logger.info(
        f"ACTION={action} | "
        f"USER={user} | "
        f"DETAILS={details}"
    )