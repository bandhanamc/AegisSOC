from sqlalchemy.orm import Session


from app.models.detection_rule import DetectionRule
from app.models.detection_rule_version import DetectionRuleVersion
from app.models.vulnerability import Vulnerability


from app.ai.knowledge.knowledge_engine import KnowledgeEngine
from app.ai.detection_engine.detection_engine import DetectionEngine



# ==========================================================
# Detection Rule CRUD
# ==========================================================


def create_detection_rule(
    db: Session,
    rule
):

    detection_rule = DetectionRule(

        name=rule.name,

        description=rule.description,

        rule_type=rule.rule_type,

        severity=rule.severity,

        query=rule.query,

        enabled=rule.enabled
    )


    db.add(detection_rule)

    db.commit()

    db.refresh(detection_rule)


    return detection_rule




def get_detection_rules(
    db: Session
):

    return (

        db.query(DetectionRule)

        .order_by(
            DetectionRule.created_at.desc()
        )

        .all()
    )




def get_detection_rule(
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




def update_detection_rule(
    db: Session,
    rule_id: int,
    rule
):

    detection_rule = get_detection_rule(
        db,
        rule_id
    )


    if not detection_rule:

        return None



    #
    # Update current rule
    #

    for key, value in rule.model_dump(
        exclude_unset=True
    ).items():


        setattr(
            detection_rule,
            key,
            value
        )



    db.commit()

    db.refresh(detection_rule)



    #
    # Create version history
    #

    current_version = (

        db.query(
            DetectionRuleVersion
        )

        .filter(
            DetectionRuleVersion.rule_id ==
            detection_rule.id
        )

        .count()
    )


    rule_version = DetectionRuleVersion(

        rule_id=detection_rule.id,

        version=current_version + 1,

        name=detection_rule.name,

        description=detection_rule.description,

        rule_type=detection_rule.rule_type,

        severity=detection_rule.severity,

        query=detection_rule.query,

        enabled=detection_rule.enabled

    )


    db.add(rule_version)

    db.commit()



    return detection_rule





def delete_detection_rule(
    db: Session,
    rule_id: int
):

    detection_rule = get_detection_rule(
        db,
        rule_id
    )


    if not detection_rule:

        return None



    db.delete(detection_rule)

    db.commit()


    return detection_rule





# ==========================================================
# Detection Rule Version History
# ==========================================================


def get_detection_rule_history(
    db: Session,
    rule_id: int
):


    return (

        db.query(
            DetectionRuleVersion
        )

        .filter(
            DetectionRuleVersion.rule_id ==
            rule_id
        )

        .order_by(
            DetectionRuleVersion.version.desc()
        )

        .all()
    )





# ==========================================================
# AI Detection Service
# ==========================================================


knowledge_engine = KnowledgeEngine()


detection_engine = DetectionEngine()




def generate_ai_detection(

    db: Session,

    vulnerability_id: int,

    detection_type: str

):


    vulnerability = (

        db.query(Vulnerability)

        .filter(
            Vulnerability.id ==
            vulnerability_id
        )

        .first()

    )


    if vulnerability is None:


        return {

            "error":
            "Vulnerability not found"

        }



    context = knowledge_engine.build_context(

        db,

        vulnerability_id

    )



    result = detection_engine.generate_detection(

        detection_type=detection_type,

        title=context["vulnerability"].title,

        description=context["vulnerability"].description,

        mitre=context["mitre"]

    )


    return result