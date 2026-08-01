from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session

import shutil
import os

from app.database.database import get_db
from app.dependencies.auth import get_current_user

from app.parsers.parser_factory import ParserFactory
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



@router.post("/scan")
def upload_scan_report(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    file_path = None

    try:

        # Save uploaded file

        file_path = os.path.join(
            UPLOAD_DIR,
            file.filename
        )


        with open(
            file_path,
            "wb"
        ) as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )



        # Select parser dynamically

        try:

            parser = ParserFactory.get_parser(
                file.filename
            )

        except ValueError as e:

            raise HTTPException(
                status_code=400,
                detail=str(e)
            )



        # Parse report

        findings = parser(
            file_path
        )



        if not findings:

            raise HTTPException(
                status_code=400,
                detail="No findings found in uploaded report"
            )



        # Import findings into database

        import_result = import_findings(
            db,
            findings
        )



        return {

            "filename": file.filename,

            "total_findings": len(findings),

            "imported_into_database":
                import_result["imported"],

            "duplicates_skipped":
                import_result["skipped"],

            "message":
                "Security report imported successfully",

            "sample":
                findings[:5]

        }



    except HTTPException:

        raise



    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )



    finally:

        # Remove uploaded file after processing

        if file_path and os.path.exists(file_path):

            os.remove(file_path)