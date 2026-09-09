import unittest
from datetime import datetime
from uuid import uuid4

from database import SessionLocal
from models import User
from repositories import (
    create_inspection,
    get_inspection,
    save_compliance_results,
    save_declarations,
    save_image_metadata,
    save_ocr_observations,
    save_report,
)


class M4RepositoryRetrievalTest(unittest.TestCase):
    def test_m4_get_inspection_returns_full_nested_graph(self):
        db = SessionLocal()
        try:
            unique = uuid4().hex[:8]
            user = User(
                full_name='M4 Regression User',
                email=f'm4-regression-{unique}@example.com',
                password_hash='hash',
                role='admin',
            )
            db.add(user)
            db.commit()
            db.refresh(user)

            inspection = create_inspection(
                db,
                user_id=user.id,
                inspection_code=f'M4-RETRIEVAL-{unique}',
                facility_name='Regression Facility Alpha',
                inspection_type='Compliance',
                status='pending',
                scheduled_at=datetime.utcnow(),
            )

            image = save_image_metadata(
                db,
                inspection_id=inspection.id,
                image_url=f'storage/images/{inspection.inspection_code}.jpg',
                caption='Mock OCR source image',
            )

            blocks = save_ocr_observations(
                db,
                inspection_image_id=image.id,
                blocks=[{
                    'text': 'Violation observed in Zone A',
                    'confidence': 95,
                    'page': 1,
                    'block_no': 1,
                    'bbox': {'x': 1, 'y': 2, 'w': 10, 'h': 12},
                    'extracted_data': {'zone': 'A', 'detected': True},
                }],
            )

            declarations = save_declarations(
                db,
                inspection_id=inspection.id,
                declarations=[{
                    'field_name': 'facility_name',
                    'field_value': 'Regression Facility Alpha',
                    'evidence_text': 'Evidence text from declaration payload',
                    'confidence': 90,
                    'declaration_type': 'declaration',
                }],
            )

            results = save_compliance_results(
                db,
                inspection_id=inspection.id,
                results=[{
                    'compliance_status': 'FAIL',
                    'compliance_score': 35,
                    'violation_count': 2,
                    'remarks': 'M4 retrieval failure',
                    'rule_id': 'RULE-001',
                    'legal_reference': 'Gazette 2026/1',
                    'evidence_region_ids': [1],
                }],
            )

            report = save_report(
                db,
                inspection_id=inspection.id,
                report_file_path=f'storage/reports/{inspection.inspection_code}.json',
                report_type='inspection_report',
                status='generated',
                report_json={'status': 'generated', 'compliance_status': results[0].compliance_status},
            )

            retrieved = get_inspection(db, inspection.id)

            self.assertIsNotNone(retrieved)
            self.assertEqual(inspection.id, retrieved.id)
            self.assertEqual(1, len(retrieved.images))
            self.assertEqual(1, len(retrieved.declarations))
            self.assertEqual(1, len(retrieved.results))
            self.assertEqual(1, len(retrieved.reports))
            self.assertEqual('FAIL', retrieved.results[0].compliance_status)
            self.assertEqual('RULE-001', retrieved.results[0].rule_id)
            self.assertEqual('M4 retrieval failure', retrieved.results[0].remarks)
            self.assertEqual(1, len(blocks))
            self.assertEqual(1, len(declarations))
            self.assertEqual(1, len(results))
            self.assertEqual('storage/reports/' + inspection.inspection_code + '.json', report.report_file_path)
        finally:
            db.close()


if __name__ == '__main__':
    unittest.main()
