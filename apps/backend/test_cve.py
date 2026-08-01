from app.services.cve_intelligence_service import CVEIntelligence


cve=CVEIntelligence()


print(
    cve.enrich(
        "CVE-2021-44228"
    )
)