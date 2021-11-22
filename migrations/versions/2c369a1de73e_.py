"""empty message

Revision ID: 2c369a1de73e
Revises: 17413c6bd0ab
Create Date: 2021-11-11 11:40:42.119474

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2c369a1de73e'
down_revision = '17413c6bd0ab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('rental', 'videos_checked_out_count')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('rental', sa.Column('videos_checked_out_count', sa.INTEGER(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
