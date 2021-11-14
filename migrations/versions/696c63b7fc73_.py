"""empty message

Revision ID: 696c63b7fc73
Revises: f71d63741ed2
Create Date: 2021-11-14 14:50:26.184451

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '696c63b7fc73'
down_revision = 'f71d63741ed2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('video', sa.Column('id', sa.Integer(), nullable=False))
    op.add_column('video', sa.Column('total_inventory', sa.Integer(), nullable=True))
    op.drop_column('video', 'inventory')
    op.drop_column('video', 'video_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('video', sa.Column('video_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('video', sa.Column('inventory', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('video', 'total_inventory')
    op.drop_column('video', 'id')
    # ### end Alembic commands ###
