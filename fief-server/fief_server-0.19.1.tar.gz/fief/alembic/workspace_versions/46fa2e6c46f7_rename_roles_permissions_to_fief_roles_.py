"""Rename roles_permissions to fief_roles_permissions

Revision ID: 46fa2e6c46f7
Revises: 7f4cbde3bcb7
Create Date: 2022-06-08 15:25:26.573302

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

import fief

# revision identifiers, used by Alembic.
revision = "46fa2e6c46f7"
down_revision = "7f4cbde3bcb7"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.rename_table("roles_permissions", "fief_roles_permissions")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.rename_table("fief_roles_permissions", "roles_permissions")
    # ### end Alembic commands ###
