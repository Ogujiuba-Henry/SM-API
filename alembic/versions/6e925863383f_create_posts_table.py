"""create posts table

Revision ID: 6e925863383f
Revises: 
Create Date: 2022-07-26 21:20:57.080184

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6e925863383f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('postss',sa.Column('id',sa.Integer(),nullable=False,primary_key=True),sa.Column('title',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
