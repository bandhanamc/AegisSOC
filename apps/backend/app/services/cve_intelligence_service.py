import requests


class CVEIntelligence:


    def enrich(self, cve_id):

        if not cve_id:
            return {}


        try:

            url = (
                "https://services.nvd.nist.gov/rest/json/"
                "cves/2.0?"
                f"cveId={cve_id}"
            )


            response = requests.get(
                url,
                timeout=10
            )


            data=response.json()


            vulnerabilities=data.get(
                "vulnerabilities",
                []
            )


            if not vulnerabilities:
                return {}


            cve = vulnerabilities[0]["cve"]


            weaknesses = cve.get(
                "weaknesses",
                []
            )


            cwes=[]


            for weakness in weaknesses:

                for desc in weakness.get("description", []):

                    cwes.append(
                        desc.get("value")
                    )


            return {

                "cwe": cwes[0]
                if cwes else None

            }


        except Exception:

            return {}