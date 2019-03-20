"""

Revision ID: v0.0.11_2b12003a3b8
Revises: 7748bc1918ad
Create Date: 2019-03-14 10:36:31.044431

"""
import sys
from alembic import op
import sqlalchemy as sa
from pathlib import Path

root_path = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(root_path))

import backend.model



# revision identifiers, used by Alembic.
revision = 'v0.0.11_2b12003a3b8'
down_revision = '7748bc1918ad'
branch_labels = ('v0.0.11',)
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('_ax_field_types')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('_ax_field_types',
    sa.Column('uuid', sa.CHAR(length=32), nullable=False),
    sa.Column('name', sa.VARCHAR(length=255), nullable=True),
    sa.Column('default_name', sa.VARCHAR(length=255), nullable=True),
    sa.Column('default_db_name', sa.VARCHAR(length=255), nullable=True),
    sa.Column('order', sa.INTEGER(), nullable=True),
    sa.Column('value_type', sa.VARCHAR(length=255), nullable=True),
    sa.Column('web_element', sa.VARCHAR(length=255), nullable=True),
    sa.Column('comparator', sa.VARCHAR(length=255), nullable=True),
    sa.Column('is_group', sa.BOOLEAN(), nullable=True),
    sa.Column('field_group_name', sa.VARCHAR(length=255), nullable=True),
    sa.Column('icon', sa.VARCHAR(length=255), nullable=True),
    sa.Column('is_inline_editable', sa.BOOLEAN(), nullable=True),
    sa.Column('is_backend_available', sa.BOOLEAN(), nullable=True),
    sa.Column('is_updated_always', sa.BOOLEAN(), nullable=True),
    sa.Column('is_always_whole_row', sa.BOOLEAN(), nullable=True),
    sa.CheckConstraint('is_always_whole_row IN (0, 1)'),
    sa.CheckConstraint('is_backend_available IN (0, 1)'),
    sa.CheckConstraint('is_group IN (0, 1)'),
    sa.CheckConstraint('is_inline_editable IN (0, 1)'),
    sa.CheckConstraint('is_updated_always IN (0, 1)'),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('uuid')
    )
    # ### end Alembic commands ###