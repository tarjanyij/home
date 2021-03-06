"""modify model SensorConfig

Revision ID: 3e85c818a5a9
Revises: aaca65d506ca
Create Date: 2021-02-26 14:21:15.383828

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3e85c818a5a9'
down_revision = 'aaca65d506ca'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sensor_config', sa.Column('display_order', sa.Integer(), nullable=True))
    op.add_column('sensor_config', sa.Column('tick', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('sensor_config', 'tick')
    op.drop_column('sensor_config', 'display_order')
    # ### end Alembic commands ###
