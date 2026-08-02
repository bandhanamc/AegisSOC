from sqlalchemy.orm import Session

from app.models.detection_rule import DetectionRule


class RuleRepository:


    def create(
        self,
        db: Session,
        rule: DetectionRule
    ):

        db.add(rule)
        db.commit()
        db.refresh(rule)

        return rule


    def get_all(
        self,
        db: Session
    ):

        return (
            db.query(DetectionRule)
            .order_by(
                DetectionRule.created_at.desc()
            )
            .all()
        )


    def get(
        self,
        db: Session,
        rule_id: int
    ):

        return (
            db.query(DetectionRule)
            .filter(
                DetectionRule.id == rule_id
            )
            .first()
        )


    def delete(
        self,
        db: Session,
        rule_id: int
    ):

        rule = self.get(
            db,
            rule_id
        )

        if not rule:
            return None

        db.delete(rule)
        db.commit()

        return rule