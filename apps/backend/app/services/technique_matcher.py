from typing import List, Dict


class TechniqueMatcher:
    """
    Behavior based MITRE ATT&CK technique matcher.
    """


    BEHAVIOR_MAP = {


        "T1059.001": [
            "powershell",
            "powershell.exe",
            "invoke-expression",
            "invoke-command",
            ".ps1"
        ],


        "T1059": [
            "cmd.exe",
            "command shell",
            "windows command",
            "shell"
        ],


        "T1105": [
            "download",
            "downloaded",
            "download file",
            "transfer file",
            "remote file",
            "payload download"
        ],


        "T1204.002": [
            "opened attachment",
            "malicious file",
            "user executed file",
            "clicked attachment"
        ],


        "T1053": [
            "scheduled task",
            "task scheduler",
            "cron"
        ],


        "T1021": [
            "remote desktop",
            "rdp",
            "smb",
            "remote service"
        ]

    }



    def __init__(self):
        pass



    def match(
        self,
        text: str,
        techniques: List[Dict]
    ):


        text = text.lower()


        matched_ids = []


        # Behavior detection

        for technique_id, keywords in self.BEHAVIOR_MAP.items():


            for keyword in keywords:


                if keyword.lower() in text:

                    matched_ids.append(
                        {
                            "technique_id": technique_id,
                            "score": 10,
                            "reason": f"Matched behavior keyword: {keyword}"
                        }
                    )

                    break



        results=[]


        # Resolve MITRE details

        for match in matched_ids:


            for technique in techniques:


                if technique.get("technique_id") == match["technique_id"]:


                    results.append(
                        {
                            "technique_id":
                                technique["technique_id"],

                            "name":
                                technique["name"],

                            "score":
                                match["score"],

                            "reason":
                                match["reason"]
                        }
                    )



        return results