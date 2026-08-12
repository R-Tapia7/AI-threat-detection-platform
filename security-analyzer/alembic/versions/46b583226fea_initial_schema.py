from alembic import op
import sqlalchemy as sa

revision = 'initial_schema'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        CREATE TABLE IF NOT EXISTS analysis_results (
            id VARCHAR NOT NULL,
            log_id VARCHAR NOT NULL,
            timestamp TIMESTAMP WITHOUT TIME ZONE NOT NULL,
            ip VARCHAR NOT NULL,
            user_id VARCHAR NOT NULL,
            action VARCHAR NOT NULL,
            status VARCHAR NOT NULL,
            threat_level VARCHAR NOT NULL,
            rule_triggered VARCHAR,
            ai_report VARCHAR,
            created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
            PRIMARY KEY (id)
        )
    """)


def downgrade():
    op.execute("DROP TABLE IF EXISTS analysis_results")
