"""Car Table

Revision ID: 0ad50c9efaa2
Revises: 5bef28ec7c00
Create Date: 2022-12-23 12:01:48.841098

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0ad50c9efaa2'
down_revision = '5bef28ec7c00'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('car',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('objectId', sa.String(length=25), nullable=False),
    sa.Column('createdAt', sa.String(length=25), nullable=False),
    sa.Column('updatedAt', sa.String(length=25), nullable=False),
    sa.Column('year', sa.INTEGER(), nullable=True),
    sa.Column('make', sa.String(length=20), nullable=True),
    sa.Column('category', sa.String(length=25), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('car')
    # ### end Alembic commands ###
