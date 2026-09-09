from typing import Iterable

from sqlalchemy.orm import Session

from models import (
    Inspection,
    InspectionImage,
    OcrTextBlock,
    Declaration,
    ComplianceResult,
    Report,
)


def create_inspection(session: Session, *, user_id: int, inspection_code: str,
                      facility_name: str, inspection_type: str, status: str = 'CREATED',
                      scheduled_at=None) -> Inspection:
    inspection = Inspection(
        user_id=user_id,
        inspection_code=inspection_code,
        facility_name=facility_name,
        inspection_type=inspection_type,
        status=status,
        scheduled_at=scheduled_at,
    )
    session.add(inspection)
    session.commit()
    session.refresh(inspection)
    return inspection


def save_image_metadata(session: Session, *, inspection_id: int, image_url: str,
                         caption: str | None = None) -> InspectionImage:
    image = InspectionImage(
        inspection_id=inspection_id,
        image_url=image_url,
        caption=caption,
    )
    session.add(image)
    session.commit()
    session.refresh(image)
    return image


def save_ocr_observations(session: Session, *, inspection_image_id: int,
                           blocks: Iterable[dict]) -> list[OcrTextBlock]:
    records = []
    for block in blocks:
        record = OcrTextBlock(
            inspection_image_id=inspection_image_id,
            text=block.get('text'),
            confidence=block.get('confidence'),
            page=block.get('page'),
            block_no=block.get('block_no'),
            bbox=block.get('bbox'),
            extracted_data=block.get('extracted_data'),
        )
        session.add(record)
        records.append(record)
    session.commit()
    for record in records:
        session.refresh(record)
    return records


def save_declarations(session: Session, *, inspection_id: int,
                       declarations: Iterable[dict]) -> list[Declaration]:
    records = []
    for item in declarations:
        record = Declaration(
            inspection_id=inspection_id,
            field_name=item.get('field_name'),
            field_value=item.get('field_value'),
            evidence_text=item.get('evidence_text'),
            confidence=item.get('confidence'),
            declaration_type=item.get('declaration_type', 'declaration'),
        )
        session.add(record)
        records.append(record)
    session.commit()
    for record in records:
        session.refresh(record)
    return records


def save_compliance_results(session: Session, *, inspection_id: int,
                             results: Iterable[dict]) -> list[ComplianceResult]:
    records = []
    for item in results:
        record = ComplianceResult(
            inspection_id=inspection_id,
            compliance_status=item.get('compliance_status', 'REVIEW'),
            compliance_score=item.get('compliance_score'),
            violation_count=item.get('violation_count', 0),
            remarks=item.get('remarks'),
            rule_id=item.get('rule_id'),
            legal_reference=item.get('legal_reference'),
            evidence_region_ids=item.get('evidence_region_ids'),
        )
        session.add(record)
        records.append(record)
    session.commit()
    for record in records:
        session.refresh(record)
    return records


def get_inspection(session: Session, inspection_id: int) -> Inspection | None:
    from models import Inspection
    return session.get(Inspection, inspection_id)


def list_inspections(session: Session, limit: int = 50) -> list[Inspection]:
    return session.query(Inspection).order_by(Inspection.created_at.desc()).limit(limit).all()


def get_dashboard_summary(session: Session) -> dict:
    total = session.query(Inspection).count()
    results = session.query(ComplianceResult).count()
    failed = session.query(ComplianceResult).filter(ComplianceResult.compliance_status == 'FAIL').count()
    review = session.query(ComplianceResult).filter(ComplianceResult.compliance_status == 'REVIEW').count()
    return {
        'total_inspections': total,
        'total_results': results,
        'failed': failed,
        'review': review,
    }


def save_report(session: Session, *, inspection_id: int, report_file_path: str,
                report_type: str = 'inspection_report', status: str = 'generated',
                report_json: dict | None = None) -> Report:
    report = Report(
        inspection_id=inspection_id,
        report_type=report_type,
        report_file_path=report_file_path,
        status=status,
        report_json=report_json,
    )
    session.add(report)
    session.commit()
    session.refresh(report)
    return report
