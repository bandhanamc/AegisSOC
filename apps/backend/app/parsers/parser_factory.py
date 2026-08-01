from app.parsers.nessus_parser import parse_nessus_file


class ParserFactory:

    @staticmethod
    def get_parser(filename: str):

        filename = filename.lower()

        if filename.endswith(".nessus"):
            return parse_nessus_file

        raise ValueError(
            f"Unsupported file type: {filename}"
        )