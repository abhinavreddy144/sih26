"""create stable project tables

Revision ID: 001
Revises: 
Create Date: 2026-09-09 00:00:00.000000

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('full_name', sa.String(length=150), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False, unique=True),
        sa.Column('password_hash', sa.String(length=255), nullable=True),
        sa.Column('role', sa.String(length=50), nullable=False, server_default='admin'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
    )

    op.create_table(
        'inspections',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('inspection_code', sa.String(length=100), nullable=False, unique=True),
        sa.Column('facility_name', sa.String(length=150), nullable=False),
        sa.Column('inspection_type', sa.String(length=50), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='CREATED'),
        sa.Column('scheduled_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
    )

    op.create_table(
        'inspection_images',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('inspection_id', sa.Integer(), sa.ForeignKey('inspections.id', ondelete='CASCADE'), nullable=False),
        sa.Column('image_url', sa.String(length=500), nullable=False),
        sa.Column('caption', sa.String(length=200), nullable=True),
        sa.Column('uploaded_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
    )

    op.create_table(
        'ocr_text_blocks',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('inspection_image_id', sa.Integer(), sa.ForeignKey('inspection_images.id', ondelete='CASCADE'), nullable=False),
        sa.Column('text', sa.Text(), nullable=False),
        sa.Column('confidence', sa.Integer(), nullable=True),
        sa.Column('page', sa.Integer(), nullable=True),
        sa.Column('block_no', sa.Integer(), nullable=True),
        sa.Column('bbox', sa.JSON(), nullable=True),
        sa.Column('extracted_data', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
    )

    op.create_table(
        'declarations',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('inspection_id', sa.Integer(), sa.ForeignKey('inspections.id', ondelete='CASCADE'), nullable=False),
        sa.Column('field_name', sa.String(length=120), nullable=False),
        sa.Column('field_value', sa.Text(), nullable=False),
        sa.Column('evidence_text', sa.Text(), nullable=True),
        sa.Column('confidence', sa.Integer(), nullable=True),
        sa.Column('declaration_type', sa.String(length=80), nullable=False, server_default='declaration'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
    )

    op.create_table(
        'compliance_results',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('inspection_id', sa.Integer(), sa.ForeignKey('inspections.id', ondelete='CASCADE'), nullable=False, unique=True),
        sa.Column('compliance_status', sa.String(length=50), nullable=False),
        sa.Column('compliance_score', sa.Integer(), nullable=True),
        sa.Column('violation_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('rule_id', sa.String(length=120), nullable=True),
        sa.Column('legal_reference', sa.String(length=500), nullable=True),
        sa.Column('evidence_region_ids', sa.JSON(), nullable=True),
        sa.Column('remarks', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
    )

    op.create_table(
        'reports',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('inspection_id', sa.Integer(), sa.ForeignKey('inspections.id', ondelete='CASCADE'), nullable=False),
        sa.Column('report_type', sa.String(length=80), nullable=False, server_default='inspection_report'),
        sa.Column('report_file_path', sa.String(length=500), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='generated'),
        sa.Column('generated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('report_json', sa.JSON(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table('reports')
    op.drop_table('compliance_results')
    op.drop_table('declarations')
    op.drop_table('ocr_text_blocks')
    op.drop_table('inspection_images')
    op.drop_table('inspections')
    op.drop_table('users')
