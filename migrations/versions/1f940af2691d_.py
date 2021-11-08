"""empty message

Revision ID: 1f940af2691d
Revises: dbf10158564b
Create Date: 2021-11-06 19:02:45.696703

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1f940af2691d'
down_revision = 'dbf10158564b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('customer', sa.Column('phone', sa.String(length=14), nullable=True))
    op.drop_column('customer', 'phone_number')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('customer', sa.Column('phone_number', sa.VARCHAR(length=14), autoincrement=False, nullable=True))
    op.drop_column('customer', 'phone')
    # ### end Alembic commands ###
