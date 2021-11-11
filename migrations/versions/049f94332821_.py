"""empty message

Revision ID: 049f94332821
Revises: 
Create Date: 2021-11-10 17:40:07.478893

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '049f94332821'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('customer',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('postal_code', sa.String(), nullable=False),
    sa.Column('phone', sa.String(), nullable=False),
    sa.Column('register_at', sa.DateTime(), nullable=True),
    sa.Column('number_of_rentals', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('video',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('release_date', sa.DateTime(), nullable=True),
    sa.Column('total_inventory', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rental',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.Column('video_id', sa.Integer(), nullable=False),
    sa.Column('due_date', sa.DateTime(), nullable=False),
    sa.Column('status', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['customer.id'], ),
    sa.ForeignKeyConstraint(['video_id'], ['video.id'], ),
    sa.PrimaryKeyConstraint('id', 'customer_id', 'video_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('rental')
    op.drop_table('video')
    op.drop_table('customer')
    # ### end Alembic commands ###
