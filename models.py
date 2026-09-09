from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON, func
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    full_name = Column(String(150), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=True)
    role = Column(String(50), nullable=False, default='admin')
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    inspections = relationship('Inspection', back_populates='user')


class Inspection(Base):
    __tablename__ = 'inspections'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    inspection_code = Column(String(100), unique=True, nullable=False)
    facility_name = Column(String(150), nullable=False)
    inspection_type = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False, default='CREATED')
    scheduled_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    user = relationship('User', back_populates='inspections')
    images = relationship('InspectionImage', back_populates='inspection', cascade='all, delete-orphan')
    results = relationship('ComplianceResult', back_populates='inspection', cascade='all, delete-orphan')
    declarations = relationship('Declaration', back_populates='inspection', cascade='all, delete-orphan')
    reports = relationship('Report', back_populates='inspection', cascade='all, delete-orphan')


class InspectionImage(Base):
    __tablename__ = 'inspection_images'

    id = Column(Integer, primary_key=True)
    inspection_id = Column(
        Integer,
        ForeignKey('inspections.id', ondelete='CASCADE'),
        nullable=False,
    )
    image_url = Column(String(500), nullable=False)
    caption = Column(String(200), nullable=True)
    uploaded_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    inspection = relationship('Inspection', back_populates='images')
    blocks = relationship('OcrTextBlock', back_populates='inspection_image', cascade='all, delete-orphan')


class OcrTextBlock(Base):
    __tablename__ = 'ocr_text_blocks'

    id = Column(Integer, primary_key=True)
    inspection_image_id = Column(
        Integer,
        ForeignKey('inspection_images.id', ondelete='CASCADE'),
        nullable=False,
    )
    text = Column(Text, nullable=False)
    confidence = Column(Integer, nullable=True)
    page = Column(Integer, nullable=True)
    block_no = Column(Integer, nullable=True)
    bbox = Column(JSON, nullable=True)
    extracted_data = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    inspection_image = relationship('InspectionImage', back_populates='blocks')


class Declaration(Base):
    __tablename__ = 'declarations'

    id = Column(Integer, primary_key=True)
    inspection_id = Column(
        Integer,
        ForeignKey('inspections.id', ondelete='CASCADE'),
        nullable=False,
    )
    field_name = Column(String(120), nullable=False)
    field_value = Column(Text, nullable=False)
    evidence_text = Column(Text, nullable=True)
    confidence = Column(Integer, nullable=True)
    declaration_type = Column(String(80), nullable=False, default='declaration')
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    inspection = relationship('Inspection', back_populates='declarations')


class ComplianceResult(Base):
    __tablename__ = 'compliance_results'

    id = Column(Integer, primary_key=True)
    inspection_id = Column(
        Integer,
        ForeignKey('inspections.id', ondelete='CASCADE'),
        nullable=False,
        unique=True,
    )
    compliance_status = Column(String(50), nullable=False)
    compliance_score = Column(Integer, nullable=True)
    violation_count = Column(Integer, nullable=False, default=0)
    rule_id = Column(String(120), nullable=True)
    legal_reference = Column(String(500), nullable=True)
    evidence_region_ids = Column(JSON, nullable=True)
    remarks = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    inspection = relationship('Inspection', back_populates='results')


class Report(Base):
    __tablename__ = 'reports'

    id = Column(Integer, primary_key=True)
    inspection_id = Column(
        Integer,
        ForeignKey('inspections.id', ondelete='CASCADE'),
        nullable=False,
    )
    report_type = Column(String(80), nullable=False, default='inspection_report')
    report_file_path = Column(String(500), nullable=False)
    status = Column(String(50), nullable=False, default='generated')
    generated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    report_json = Column(JSON, nullable=True)

    inspection = relationship('Inspection', back_populates='reports')
