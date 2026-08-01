from app.database.database import SessionLocal

from app.models.vulnerability import Vulnerability

from app.ai.mitre_mapper import MitreMapper



db = SessionLocal()


try:

    vulnerability = db.query(
        Vulnerability
    ).first()


    if vulnerability is None:

        print("No vulnerability found in database")

        exit()



    print("\nTesting Vulnerability:")
    print("----------------------")
    print("ID:", vulnerability.id)
    print("Title:", vulnerability.title)
    print("Severity:", vulnerability.severity)



    mapper = MitreMapper()



    results = mapper.map_vulnerability(
        db,
        vulnerability,
        top_k=5
    )



    print("\nMITRE Mapping Results:")
    print("----------------------")


    for result in results:

        print(result)



finally:

    db.close()