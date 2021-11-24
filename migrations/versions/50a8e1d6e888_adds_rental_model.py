"""adds Rental model

Revision ID: 50a8e1d6e888
Revises: 1cabe7a100f9
Create Date: 2021-11-09 11:51:56.056083

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '50a8e1d6e888'
down_revision = '1cabe7a100f9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('rentals',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.Column('video_id', sa.Integer(), nullable=False),
    sa.Column('due_date', sa.String(), nullable=False),
    sa.Column('videos_checked_out_count', sa.Integer(), nullable=True),
    sa.Column('available_inventory', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['customer.id'], ),
    sa.ForeignKeyConstraint(['video_id'], ['video.id'], ),
    sa.PrimaryKeyConstraint('id', 'customer_id', 'video_id')
    )
    op.drop_table('rental')
    op.add_column('customer', sa.Column('phone', sa.String(length=60), nullable=True))
    op.drop_column('customer', 'phone_number')
    op.add_column('video', sa.Column('release_date', sa.Date(), nullable=True))
    op.add_column('video', sa.Column('title', sa.String(length=30), nullable=True))
    op.add_column('video', sa.Column('total_inventory', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('video', 'total_inventory')
    op.drop_column('video', 'title')
    op.drop_column('video', 'release_date')
    op.add_column('customer', sa.Column('phone_number', sa.VARCHAR(length=15), autoincrement=False, nullable=True))
    op.drop_column('customer', 'phone')
    op.create_table('rental',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.PrimaryKeyConstraint('id', name='rental_pkey')
    )
    op.drop_table('rentals')
    # ### end Alembic commands ###
