from alembic import op
import sqlalchemy as sa

revision = '1975ea83b712'
down_revision = None
branch_labels = None


def upgrade():
    op.add_column("teacher", sa.Column("employment", sa.ARRAY(sa.String)))


def downgrade():
    op.drop_column("teacher", "employment")
