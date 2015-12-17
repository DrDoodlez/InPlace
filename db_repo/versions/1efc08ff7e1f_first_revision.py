"""First revision

Revision ID: 1efc08ff7e1f
Revises: 283c496f7afe
Create Date: 2015-12-17 14:58:28.928978

"""

# revision identifiers, used by Alembic.
revision = '1efc08ff7e1f'
down_revision = '283c496f7afe'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('login', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('password', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('login')
    )
    op.create_table('place',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('description', sa.String(length=128), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('author', sa.String(length=64), nullable=True),
    sa.Column('text', sa.String(length=64), nullable=True),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('place_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['place_id'], ['place.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('text')
    )
    op.create_table('event',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('description', sa.String(length=64), nullable=True),
    sa.Column('date', sa.String(length=64), nullable=True),
    sa.Column('place_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['place_id'], ['place.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('description')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('event')
    op.drop_table('comment')
    op.drop_table('place')
    op.drop_table('user')
    ### end Alembic commands ###