"""Add workspaces

Revision ID: 2f1a7a9c7b1a
Revises: 1a31ce608336
Create Date: 2024-09-22 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = "2f1a7a9c7b1a"
down_revision = "1a31ce608336"
branch_labels = None
depends_on = None


def upgrade():
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')

    op.create_table(
        "workspace",
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column("owner_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(["owner_id"], ["user.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.add_column(
        "item",
        sa.Column("workspace_id", postgresql.UUID(as_uuid=True), nullable=True),
    )
    op.create_foreign_key(
        None, "item", "workspace", ["workspace_id"], ["id"], ondelete="CASCADE"
    )


def downgrade():
    op.drop_constraint(None, "item", type_="foreignkey")
    op.drop_column("item", "workspace_id")
    op.drop_table("workspace")
