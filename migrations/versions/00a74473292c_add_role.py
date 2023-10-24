"""add role

Revision ID: 00a74473292c
Revises:
Create Date: 2023-10-13 08:49:16.951355

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "00a74473292c"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "role",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("role", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_role_created_at"), ["created_at"], unique=False)
        batch_op.create_index(batch_op.f("ix_role_title"), ["title"], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("role", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_role_title"))
        batch_op.drop_index(batch_op.f("ix_role_created_at"))

    op.drop_table("role")
    # ### end Alembic commands ###