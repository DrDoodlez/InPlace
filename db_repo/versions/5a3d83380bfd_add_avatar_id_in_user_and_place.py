"""add avatar_id in user and place

Revision ID: 5a3d83380bfd
Revises: 1f78da733f20
Create Date: 2015-12-18 22:00:39.640124

"""

# revision identifiers, used by Alembic.
revision = '5a3d83380bfd'
down_revision = '1f78da733f20'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('place', sa.Column('avatar_id', sa.String(length=64), nullable=True))
    op.add_column('user', sa.Column('avatar_id', sa.String(length=64), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'avatar_id')
    op.drop_column('place', 'avatar_id')
    ### end Alembic commands ###