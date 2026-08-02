import re


class OutputParser:

    @staticmethod
    def clean(text: str):

        if text is None:
            return ""

        text = text.strip()

        text = re.sub(
            r"```[a-zA-Z]*",
            "",
            text
        )

        text = text.replace(
            "```",
            ""
        )

        text = re.sub(
            r'^\$rules\s*=\s*"',
            "",
            text
        )

        text = re.sub(
            r'"$',
            "",
            text
        )

        return text.strip()