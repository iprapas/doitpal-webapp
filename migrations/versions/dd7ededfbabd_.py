"""empty message

Revision ID: dd7ededfbabd
Revises: 
Create Date: 2019-05-23 16:19:43.378077

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dd7ededfbabd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bookings', sa.Column('price', sa.Integer(), nullable=True))
    op.add_column('reviews', sa.Column('booking_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'reviews', 'bookings', ['booking_id'], ['id'])
    op.add_column('serving_areas', sa.Column('nborhood', sa.String(length=128), nullable=True))
    op.drop_constraint('serving_areas_nborhood_id_fkey', 'serving_areas', type_='foreignkey')
    op.drop_column('serving_areas', 'nborhood_id')
    op.add_column('taskers', sa.Column('category', sa.String(length=128), nullable=True))
    op.drop_constraint('taskers_category_id_fkey', 'taskers', type_='foreignkey')
    op.drop_column('taskers', 'category_id')
    op.drop_column('users', 'education')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('education', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('taskers', sa.Column('category_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('taskers_category_id_fkey', 'taskers', 'all_categories', ['category_id'], ['id'])
    op.drop_column('taskers', 'category')
    op.add_column('serving_areas', sa.Column('nborhood_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('serving_areas_nborhood_id_fkey', 'serving_areas', 'all_nborhoods', ['nborhood_id'], ['id'])
    op.drop_column('serving_areas', 'nborhood')
    op.drop_constraint(None, 'reviews', type_='foreignkey')
    op.drop_column('reviews', 'booking_id')
    op.drop_column('bookings', 'price')
    # ### end Alembic commands ###
