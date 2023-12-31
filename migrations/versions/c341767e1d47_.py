"""empty message

Revision ID: c341767e1d47
Revises: 
Create Date: 2023-10-26 11:07:57.939873

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c341767e1d47'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('password', sa.LargeBinary(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('device',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('device_ip', sa.String(length=255), nullable=True),
    sa.Column('device_name', sa.String(length=255), nullable=True),
    sa.Column('extra', sa.JSON(), nullable=True),
    sa.Column('is_on', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('group',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('group_name', sa.String(length=255), nullable=False),
    sa.Column('is_on', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('group_name')
    )
    op.create_table('relay_group',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('group_name', sa.String(length=255), nullable=False),
    sa.Column('is_on', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('group_name')
    )
    op.create_table('group_device_association',
    sa.Column('group_id', sa.Integer(), nullable=True),
    sa.Column('device_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['device_id'], ['device.id'], ),
    sa.ForeignKeyConstraint(['group_id'], ['group.id'], )
    )
    op.create_table('relay',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('relay_pin', sa.Integer(), nullable=False),
    sa.Column('is_on', sa.Boolean(), nullable=True),
    sa.Column('relay_name', sa.String(length=255), nullable=True),
    sa.Column('device_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['device_id'], ['device.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('relay_group_relay_association',
    sa.Column('relay_group_id', sa.Integer(), nullable=True),
    sa.Column('relay_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['relay_group_id'], ['relay_group.id'], ),
    sa.ForeignKeyConstraint(['relay_id'], ['relay.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('relay_group_relay_association')
    op.drop_table('relay')
    op.drop_table('group_device_association')
    op.drop_table('relay_group')
    op.drop_table('group')
    op.drop_table('device')
    op.drop_table('Users')
    # ### end Alembic commands ###
