"""empty message

Revision ID: 2d2c218b9bc7
Revises: 5bc1e644d4c7
Create Date: 2023-10-11 15:57:29.806532

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2d2c218b9bc7'
down_revision = '5bc1e644d4c7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('relay', sa.Column('relay_pin', sa.Integer(), nullable=False))
    op.drop_column('relay', 'relay_number')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('relay', sa.Column('relay_number', sa.INTEGER(), nullable=False))
    op.drop_column('relay', 'relay_pin')
    # ### end Alembic commands ###
