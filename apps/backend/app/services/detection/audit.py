from datetime import datetime, timezone


class DetectionAudit:

    def log(
        self,
        action: str,
        rule_type: str,
        title: str
    ):

        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "action": action,
            "rule_type": rule_type,
            "title": title
        }