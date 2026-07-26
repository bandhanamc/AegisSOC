from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session

import shutil
import os


from app.database.database import get_db
from app.dependencies.auth import get_current_user

from app.parsers.nessus_parser import parse_nessus_file
from app.services.nessus_import_service import import_findings


router = APIRouter(
    prefix="/api/v1/uploads",
    tags=["Uploads"]
)


UPLOAD_DIR = "uploads"


os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)



@router.post("/nessus")
def upload_nessus(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    try:

        file_path = os.path.join(
            UPLOAD_DIR,
            file.filename
        )


        # Save uploaded Nessus file
        with open(
            file_path,
            "wb"
        ) as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )


        # Parse Nessus XML
        findings = parse_nessus_file(
            file_path
        )


        if not findings:

            raise HTTPException(
                status_code=400,
                detail="No findings found in Nessus file"
            )


        # Import findings into database
        import_result = import_findings(
            db,
            findings
        )


        return {

            "filename": file.filename,

            "total_findings": len(findings),

            "imported_into_database": import_result["imported"],

            "duplicates_skipped": import_result["skipped"],

            "message": "Nessus report imported successfully",

            "sample": findings[:5]

        }



    except HTTPException:

        raise



    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )