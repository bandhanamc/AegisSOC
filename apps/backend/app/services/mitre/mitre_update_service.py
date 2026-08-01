import requests
import json
import os

from sqlalchemy.orm import Session

from app.models.mitre_technique import MitreTechnique



MITRE_URL = (
    "https://raw.githubusercontent.com/"
    "mitre-attack/attack-stix-data/"
    "master/enterprise-attack/"
    "enterprise-attack.json"
)



DOWNLOAD_PATH = "data/enterprise-attack.json"



def download_mitre_database():


    os.makedirs(
        "data",
        exist_ok=True
    )


    response = requests.get(
        MITRE_URL,
        timeout=60
    )


    response.raise_for_status()


    with open(
        DOWNLOAD_PATH,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            response.text
        )



    return DOWNLOAD_PATH






def update_mitre_database(
    db: Session
):


    path = download_mitre_database()


    with open(
        path,
        encoding="utf-8"
    ) as f:

        data=json.load(f)



    techniques=[]


    for obj in data["objects"]:


        if obj.get("type") != "attack-pattern":

            continue



        external=obj.get(
            "external_references",
            []
        )


        technique_id=None


        for ref in external:


            if ref.get(
                "source_name"
            )=="mitre-attack":

                technique_id=ref.get(
                    "external_id"
                )



        if not technique_id:

            continue



        name=obj.get(
            "name"
        )



        description=obj.get(
            "description",
            ""
        )



        techniques.append(

            {
                "technique_id":technique_id,

                "name":name,

                "description":description

            }

        )





    updated=0



    for t in techniques:


        existing=db.query(
            MitreTechnique
        ).filter(
            MitreTechnique.technique_id==
            t["technique_id"]
        ).first()



        if existing:


            existing.name=t["name"]

            existing.description=t["description"]


        else:


            db.add(

                MitreTechnique(
                    technique_id=t["technique_id"],
                    name=t["name"],
                    tactic="",
                    description=t["description"]
                )

            )



        updated+=1



    db.commit()



    return {

        "updated":updated,

        "total":len(techniques)

    }