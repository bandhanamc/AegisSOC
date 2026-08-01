import subprocess
import sys

import requests

from pathlib import Path

from app.database.database import SessionLocal
from app.services.mitre_import_service import MitreImportService



# ==============================
# MITRE DATASET CONFIGURATION
# ==============================


MITRE_URL = (
    "https://raw.githubusercontent.com/"
    "mitre-attack/attack-stix-data/"
    "master/enterprise-attack/"
    "enterprise-attack.json"
)



DATASET_PATH = Path(
    "data/enterprise-attack.json"
)




# ==============================
# DOWNLOAD MITRE DATASET
# ==============================


def download_mitre_dataset():

    print(
        "Downloading MITRE ATT&CK dataset"
    )


    DATASET_PATH.parent.mkdir(
        exist_ok=True
    )


    try:

        response = requests.get(
            MITRE_URL,
            timeout=120
        )


        response.raise_for_status()



        with open(
            DATASET_PATH,
            "wb"
        ) as file:

            file.write(
                response.content
            )



        print(
            "MITRE dataset downloaded successfully"
        )


        return True



    except Exception as e:


        print(
            f"MITRE download failed: {e}"
        )


        raise





# ==============================
# REBUILD FAISS INDEX
# ==============================


def rebuild_faiss():

    print(
        "Rebuilding MITRE FAISS index"
    )


    try:

        subprocess.run(

            [

                sys.executable,

                "-m",

                "app.ai.build_mitre_index"

            ],

            check=True

        )



        print(
            "FAISS index rebuilt successfully"
        )



    except subprocess.CalledProcessError as e:


        print(
            f"FAISS rebuild failed: {e}"
        )


        raise





# ==============================
# MAIN MITRE UPDATE FUNCTION
# ==============================


def update_mitre():


    print(
        "Starting MITRE update"
    )



    # Step 1
    # Download latest MITRE JSON

    download_mitre_dataset()



    # Step 2
    # Update PostgreSQL database


    db = SessionLocal()



    try:


        result = (

            MitreImportService
            .import_dataset(
                db
            )

        )


        print(
            "MITRE database update:"
        )


        print(
            result
        )



    except Exception as e:


        db.rollback()


        print(
            f"MITRE database update failed: {e}"
        )


        raise



    finally:


        db.close()




    # Step 3
    # Rebuild vector database


    rebuild_faiss()



    print(
        "MITRE update completed successfully"
    )
