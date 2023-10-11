"""empty message

Revision ID: 5bc1e644d4c7
Revises: c38f3379590f
Create Date: 2023-10-11 10:54:41.020512

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5bc1e644d4c7'
down_revision = 'c38f3379590f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('relay', sa.Column('relay_name', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('relay', 'relay_name')
    # ### end Alembic commands ###
