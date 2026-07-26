import xml.etree.ElementTree as ET


SEVERITY_MAP = {
    "0": "Informational",
    "1": "Low",
    "2": "Medium",
    "3": "High",
    "4": "Critical"
}


def parse_nessus_file(file_path):

    tree = ET.parse(file_path)

    root = tree.getroot()

    findings = []


    for report_host in root.findall(".//ReportHost"):

        host_ip = report_host.attrib.get(
            "name"
        )


        for item in report_host.findall(
            ".//ReportItem"
        ):

            severity_value = item.attrib.get(
                "severity",
                "0"
            )


            cvss_value = item.findtext(
                "cvss_base_score"
            )


            try:
                cvss_score = (
                    float(cvss_value)
                    if cvss_value
                    else None
                )

            except ValueError:
                cvss_score = None



            finding = {

                "host": host_ip,


                "plugin_id": item.attrib.get(
                    "pluginID"
                ),


                "plugin_name": item.attrib.get(
                    "pluginName"
                ),


                "severity": SEVERITY_MAP.get(
                    severity_value,
                    severity_value
                ),


                "severity_id": severity_value,


                "port": item.attrib.get(
                    "port"
                ),


                "protocol": item.attrib.get(
                    "protocol"
                ),


                "description": item.findtext(
                    "description"
                ) or "",


                "solution": item.findtext(
                    "solution"
                ) or "",


                "cve": item.findtext(
                    "cve"
                ),


                "cvss": cvss_score
            }


            findings.append(
                finding
            )


    return findings