"""keep updated timestamps correct outside SQLAlchemy

Revision ID: 002
Revises: 001
Create Date: 2026-09-09 00:00:00.000000
"""

from alembic import op


# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        CREATE OR REPLACE FUNCTION sih26034_set_updated_at()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = CURRENT_TIMESTAMP;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        """
    )
    op.execute(
        """
        CREATE TRIGGER trg_inspections_set_updated_at
        BEFORE UPDATE ON inspections
        FOR EACH ROW EXECUTE FUNCTION sih26034_set_updated_at();
        """
    )
    op.execute(
        """
        CREATE TRIGGER trg_compliance_results_set_updated_at
        BEFORE UPDATE ON compliance_results
        FOR EACH ROW EXECUTE FUNCTION sih26034_set_updated_at();
        """
    )


def downgrade() -> None:
    op.execute('DROP TRIGGER IF EXISTS trg_compliance_results_set_updated_at ON compliance_results')
    op.execute('DROP TRIGGER IF EXISTS trg_inspections_set_updated_at ON inspections')
    op.execute('DROP FUNCTION IF EXISTS sih26034_set_updated_at()')
