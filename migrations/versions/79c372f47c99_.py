"""empty message

Revision ID: 79c372f47c99
Revises: 
Create Date: 2019-05-23 01:51:41.132752

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '79c372f47c99'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bookings', sa.Column('price', sa.Integer(), nullable=True))
    op.add_column('reviews', sa.Column('booking_id', sa.Integer(), nullable=True))
    op.add_column('reviews', sa.Column('clean_rating', sa.Integer(), nullable=True))
    op.add_column('reviews', sa.Column('overall_rating', sa.Integer(), nullable=True))
    op.add_column('reviews', sa.Column('price_rating', sa.Integer(), nullable=True))
    op.add_column('reviews', sa.Column('quality_rating', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'reviews', 'bookings', ['booking_id'], ['id'])
    op.add_column('taskers', sa.Column('category', sa.String(length=128), nullable=True))
    op.add_column('taskers', sa.Column('price_per_hour', sa.Integer(), nullable=True))
    op.drop_index('ix_taskers_cname', table_name='taskers')
    op.create_unique_constraint(None, 'taskers', ['cname'])
    op.add_column('users', sa.Column('address', sa.String(length=256), nullable=True))
    op.add_column('users', sa.Column('first_name', sa.String(length=128), nullable=True))
    op.add_column('users', sa.Column('img_url', sa.String(length=512), nullable=True))
    op.add_column('users', sa.Column('last_name', sa.String(length=128), nullable=True))
    op.add_column('users', sa.Column('phone', sa.String(length=32), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'phone')
    op.drop_column('users', 'last_name')
    op.drop_column('users', 'img_url')
    op.drop_column('users', 'first_name')
    op.drop_column('users', 'address')
    op.drop_constraint(None, 'taskers', type_='unique')
    op.create_index('ix_taskers_cname', 'taskers', ['cname'], unique=True)
    op.drop_column('taskers', 'price_per_hour')
    op.drop_column('taskers', 'category')
    op.drop_constraint(None, 'reviews', type_='foreignkey')
    op.drop_column('reviews', 'quality_rating')
    op.drop_column('reviews', 'price_rating')
    op.drop_column('reviews', 'overall_rating')
    op.drop_column('reviews', 'clean_rating')
    op.drop_column('reviews', 'booking_id')
    op.drop_column('bookings', 'price')
    # ### end Alembic commands ###
