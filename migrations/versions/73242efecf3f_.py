"""empty message

Revision ID: 73242efecf3f
Revises: 92b4e432ac08
Create Date: 2020-12-17 19:04:54.175262

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '73242efecf3f'
down_revision = '92b4e432ac08'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('temperature',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('thermosensor_id', sa.String(length=50), nullable=True),
    sa.Column('temperature', sa.Float(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('password', sa.String(length=100), nullable=True),
    sa.Column('name', sa.String(length=1000), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_table('temperature')
    # ### end Alembic commands ###