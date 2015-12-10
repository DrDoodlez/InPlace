"""avatar id field

Revision ID: 53ea5e08389f
Revises: 2aa76dc5d7ba
Create Date: 2015-11-18 20:05:34.250478

"""

# revision identifiers, used by Alembic.
revision = '53ea5e08389f'
down_revision = '2aa76dc5d7ba'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('box', sa.Column('avatar_id', sa.String(length=32), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('box', 'avatar_id')
    ### end Alembic commands ###
