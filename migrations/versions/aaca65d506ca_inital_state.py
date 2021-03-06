"""inital state

Revision ID: aaca65d506ca
Revises: 
Create Date: 2021-02-23 00:03:47.989033

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aaca65d506ca'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sensor_config',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sensorname', sa.String(length=50), nullable=True),
    sa.Column('sensorid', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_sensor_config_sensorid'), 'sensor_config', ['sensorid'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('password', sa.String(length=100), nullable=True),
    sa.Column('name', sa.String(length=1000), nullable=True),
    sa.Column('token', sa.String(length=32), nullable=True),
    sa.Column('token_expiration', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_user_token'), 'user', ['token'], unique=True)
    op.create_table('temperature',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('thermosensor_id', sa.String(length=50), nullable=True),
    sa.Column('temperature', sa.Float(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['thermosensor_id'], ['sensor_config.sensorid'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('temperature')
    op.drop_index(op.f('ix_user_token'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_sensor_config_sensorid'), table_name='sensor_config')
    op.drop_table('sensor_config')
    # ### end Alembic commands ###
