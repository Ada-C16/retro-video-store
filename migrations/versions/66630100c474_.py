"""empty message

Revision ID: 66630100c474
Revises: 50a8e1d6e888
Create Date: 2021-11-11 13:37:04.012679

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '66630100c474'
down_revision = '50a8e1d6e888'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('rentals', 'available_inventory')
    op.drop_column('rentals', 'videos_checked_out_count')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('rentals', sa.Column('videos_checked_out_count', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('rentals', sa.Column('available_inventory', sa.INTEGER(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
