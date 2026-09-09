from datetime import datetime
from uuid import uuid4

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base
from models import User, Inspection, InspectionImage, ComplianceResult
from repositories import get_inspection


def run_m2_mock_flow() -> None:
    """Exercise the requested mock M2 FAIL/REVIEW result lifecycle.

    Flow:
        1. save inspection
        2. save result
        3. retrieve inspection and inspect the saved result
    """
    engine = create_engine('sqlite:///:memory:', future=True)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine, future=True)
    session = Session()

    user = User(
        full_name='M2 User',
        email='m2@example.com',
        password_hash='hash',
        role='admin',
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    mock_cases = [
        {
            'status': 'FAIL',
            'score': 35,
            'violation_count': 2,
            'remarks': 'M2 mock FAIL result',
        },
        {
            'status': 'REVIEW',
            'score': 78,
            'violation_count': 1,
            'remarks': 'M2 mock REVIEW result',
        },
    ]

    results_seen = []

    for index, mock_case in enumerate(mock_cases, start=1):
        inspection = Inspection(
            user_id=user.id,
            inspection_code=f'M2-MOCK-{mock_case["status"]}-{index}-{uuid4().hex[:8]}',
            facility_name='Mock Facility Alpha',
            inspection_type='Compliance',
            status='pending',
            scheduled_at=datetime.utcnow(),
        )
        session.add(inspection)
        session.commit()
        session.refresh(inspection)

        result = ComplianceResult(
            inspection_id=inspection.id,
            compliance_status=mock_case['status'],
            compliance_score=mock_case['score'],
            violation_count=mock_case['violation_count'],
            remarks=mock_case['remarks'],
        )
        session.add(result)
        session.commit()
        session.refresh(result)

        retrieved = get_inspection(session, inspection.id)
        if retrieved is None:
            raise AssertionError('inspection retrieve failed')

        if not retrieved.results:
            raise AssertionError('inspection result was not attached')

        attached = retrieved.results[0]
        if attached.compliance_status != mock_case['status']:
            raise AssertionError('wrong attached compliance result')

        results_seen.append({
            'inspection_id': inspection.id,
            'inspection_code': inspection.inspection_code,
            'status': attached.compliance_status,
            'score': attached.compliance_score,
            'remarks': attached.remarks,
        })

    print('M2 mock results:', results_seen)
    print('mock_m2_test_ok')


if __name__ == '__main__':
    run_m2_mock_flow()
