class InvestigationContextBuilder:


    def build(
        self,
        context
    ):


        vulnerability = context.get(
            "vulnerability"
        )

        asset = context.get(
            "asset"
        )


        data = {

            "vulnerability": {

                "id": getattr(
                    vulnerability,
                    "id",
                    None
                ),

                "title": getattr(
                    vulnerability,
                    "title",
                    None
                ),

                "description": getattr(
                    vulnerability,
                    "description",
                    None
                ),

                "severity": getattr(
                    vulnerability,
                    "severity",
                    None
                ),

                "cvss": getattr(
                    vulnerability,
                    "cvss_score",
                    None
                )
            },


            "asset": {

                "hostname": getattr(
                    asset,
                    "hostname",
                    None
                ),

                "ip": getattr(
                    asset,
                    "ip_address",
                    None
                )

            },


            "mitre": [

            ],


            "similar_vulnerabilities": [

                {
                    "title": getattr(
                        item,
                        "title",
                        None
                    ),

                    "severity": getattr(
                        item,
                        "severity",
                        None
                    )

                }

                for item in context.get(
                    "similar",
                    []
                )

            ]

        }


        return data