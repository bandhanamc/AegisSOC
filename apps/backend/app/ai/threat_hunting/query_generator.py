class QueryGenerator:


    def generate_sigma_query(
        self,
        technique
    ):


        queries = {


            "T1059.001":
            """
process where Image endswith powershell.exe
and CommandLine contains suspicious arguments
""",


            "T1003":
            """
Detect credential dumping tools:
mimikatz
procdump
lsass access
""",


            "T1041":
            """
Monitor abnormal outbound connections
and data transfer
"""

        }


        return queries.get(

            technique,

            "No hunting query available"

        )