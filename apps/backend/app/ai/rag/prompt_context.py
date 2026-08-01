class PromptContext:

    def build(
        self,
        context
    ):

        vuln = context["vulnerability"]

        asset = context["asset"]

        mitre = context["mitre"]

        similar = context["similar"]

        text = f"""

Vulnerability

Title:
{vuln.title}

Description:
{vuln.description}

Severity:
{vuln.severity}

CVE:
{vuln.cve_id}

CWE:
{vuln.cwe_id}

"""

        if asset:

            text += f"""

Affected Asset

Hostname:
{asset.hostname}

IP:
{asset.ip_address}

"""

        text += "\nMITRE Techniques\n"

        for item in mitre:

            text += (
                f"{item.technique_id}"
                f" {item.technique_name}\n"
            )

        text += "\nSimilar Vulnerabilities\n"

        for item in similar:

            text += (
                f"{item.title}\n"
            )

        return text