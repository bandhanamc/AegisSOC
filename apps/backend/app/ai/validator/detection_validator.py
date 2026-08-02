import re


class DetectionValidator:

    @staticmethod
    def validate_sigma(rule: str):

        required = [

            "title:",
            "logsource:",
            "detection:",
            "condition:"

        ]

        missing = [

            x for x in required

            if x not in rule.lower()

        ]

        return {

            "valid": len(missing) == 0,

            "missing": missing

        }


    @staticmethod
    def validate_yara(rule: str):

        required = [

            "rule",

            "meta:",

            "strings:",

            "condition:"

        ]

        missing = [

            x for x in required

            if x.lower() not in rule.lower()

        ]

        return {

            "valid": len(missing) == 0,

            "missing": missing

        }