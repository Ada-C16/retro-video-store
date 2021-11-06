"""empty message

Revision ID: 2b13ea3142d7
Revises: 27ca9680ef7b
Create Date: 2021-11-05 13:23:46.271179

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '2b13ea3142d7'
down_revision = '27ca9680ef7b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('rental', 'release_date')
    op.drop_column('rental', 'total_inventory')
    op.drop_column('rental', 'title')
    op.add_column('video', sa.Column('release_date', sa.DateTime(), nullable=True))
    op.add_column('video', sa.Column('title', sa.String(), nullable=True))
    op.add_column('video', sa.Column('total_inventory', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('video', 'total_inventory')
    op.drop_column('video', 'title')
    op.drop_column('video', 'release_date')
    op.add_column('rental', sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('rental', sa.Column('total_inventory', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('rental', sa.Column('release_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
