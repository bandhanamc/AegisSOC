from sqlalchemy.orm import Session

from app.models.vulnerability import Vulnerability
from app.models.mitre_mapping import MitreMapping



class RAGEngine:


    def search_vulnerability(
        self,
        db: Session,
        query: str,
        limit=5
    ):


        results = (
            db.query(Vulnerability)
            .filter(
                Vulnerability.title.ilike(
                    f"%{query}%"
                )
            )
            .limit(limit)
            .all()
        )


        return results




    def get_context(
        self,
        db: Session,
        query: str
    ):


        vulnerabilities = self.search_vulnerability(
            db,
            query
        )


        context=[]


        for vuln in vulnerabilities:


            mappings = db.query(
                MitreMapping
            ).filter(
                MitreMapping.vulnerability_id == vuln.id
            ).all()



            context.append(

                {

                    "title": vuln.title,

                    "description": vuln.description,

                    "severity": vuln.severity,

                    "cvss": vuln.cvss_score,

                    "cve": vuln.cve_id,

                    "cwe": vuln.cwe_id,

                    "mitre":[

                        {

                        "id":m.technique_id,

                        "name":m.technique_name

                        }

                        for m in mappings

                    ]

                }

            )


        return context