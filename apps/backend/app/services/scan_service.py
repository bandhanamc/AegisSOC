from datetime import datetime

from sqlalchemy.orm import Session

from app.models.scan import Scan
from app.schemas.scan import ScanCreate


def create_scan(
    db: Session,
    scan: ScanCreate
):

    db_scan = Scan(
        asset_id=scan.asset_id,
        scanner=scan.scanner,
        scan_type=scan.scan_type
    )

    db.add(db_scan)
    db.commit()
    db.refresh(db_scan)

    return db_scan


def get_scans(
    db: Session,
    skip: int = 0,
    limit: int = 50,
    status: str | None = None,
    scanner: str | None = None,
    asset_id: int | None = None,
    scan_type: str | None = None
):

    query = db.query(Scan)

    if status:
        query = query.filter(
            Scan.status == status
        )

    if scanner:
        query = query.filter(
            Scan.scanner == scanner
        )

    if asset_id:
        query = query.filter(
            Scan.asset_id == asset_id
        )

    if scan_type:
        query = query.filter(
            Scan.scan_type == scan_type
        )

    return (
        query
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_scan(
    db: Session,
    scan_id: int
):

    return (
        db.query(Scan)
        .filter(
            Scan.id == scan_id
        )
        .first()
    )


def update_scan_status(
    db: Session,
    scan_id: int,
    status: str
):

    scan = get_scan(
        db,
        scan_id
    )

    if not scan:
        return None

    scan.status = status

    if status == "Completed":
        scan.completed_at = datetime.utcnow()

    db.commit()
    db.refresh(scan)

    return scan


def delete_scan(
    db: Session,
    scan_id: int
):

    scan = get_scan(
        db,
        scan_id
    )

    if not scan:
        return None

    db.delete(scan)
    db.commit()

    return scan


def get_scan_count(
    db: Session
):

    return db.query(
        Scan
    ).count()