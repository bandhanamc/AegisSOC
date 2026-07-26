import re


class AlertNormalizer:
    """
    Normalizes security alert text before MITRE mapping.
    """


    def normalize(self, text):

        if not text:

            return ""


        # Convert to lowercase

        text = str(text).lower()



        # Remove special characters
        text = re.sub(
            r"[^a-z0-9\s\._-]",
            " ",
            text
        )



        # Replace multiple spaces

        text = re.sub(
            r"\s+",
            " ",
            text
        )



        # Remove duplicate words

        words = text.split()


        unique_words = []


        seen = set()


        for word in words:

            if word not in seen:

                unique_words.append(word)

                seen.add(word)



        normalized_text = " ".join(
            unique_words
        )



        return normalized_text