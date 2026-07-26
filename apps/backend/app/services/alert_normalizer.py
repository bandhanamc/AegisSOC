class AlertNormalizer:
    """
    Normalize security alerts into behavior indicators.
    """

    def normalize(self, text: str):

        text = text.lower()


        result = {
            "processes": [],
            "actions": [],
            "objects": [],
            "keywords": []
        }


        processes = [
            "powershell",
            "cmd",
            "certutil",
            "rundll32",
            "wmic",
            "bash",
            "python"
        ]


        actions = [
            "execute",
            "download",
            "upload",
            "create",
            "modify",
            "inject",
            "delete",
            "encrypt"
        ]


        objects = [
            "malware",
            "payload",
            "script",
            "credential",
            "token",
            "registry",
            "file"
        ]


        for item in processes:
            if item in text:
                result["processes"].append(item)


        for item in actions:
            if item in text:
                result["actions"].append(item)


        for item in objects:
            if item in text:
                result["objects"].append(item)


        result["keywords"] = (
            result["processes"]
            +
            result["actions"]
            +
            result["objects"]
        )


        return result