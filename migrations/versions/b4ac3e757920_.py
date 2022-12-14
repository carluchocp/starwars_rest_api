"""empty message

Revision ID: b4ac3e757920
Revises: 51d3d59fd1ae
Create Date: 2022-08-29 19:25:40.525511

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b4ac3e757920'
down_revision = '51d3d59fd1ae'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('character',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=150), nullable=False),
    sa.Column('age', sa.String(length=5), nullable=False),
    sa.Column('height', sa.String(length=5), nullable=False),
    sa.Column('eye_color', sa.String(length=50), nullable=False),
    sa.Column('hair_color', sa.String(length=50), nullable=False),
    sa.Column('gender', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('planet',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=150), nullable=False),
    sa.Column('rotation_period', sa.String(length=7), nullable=False),
    sa.Column('orbital_period', sa.String(length=7), nullable=False),
    sa.Column('gravity', sa.String(length=5), nullable=False),
    sa.Column('terrain', sa.String(length=150), nullable=False),
    sa.Column('diameter', sa.String(length=50), nullable=False),
    sa.Column('population', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('favorites',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nature', sa.Enum('character', 'planets', name='nature'), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('nature_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id', 'name', name='message_error')
    )
    op.add_column('user', sa.Column('username', sa.String(length=20), nullable=False))
    op.create_unique_constraint(None, 'user', ['username'])
    op.drop_column('user', 'is_active')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('is_active', sa.BOOLEAN(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'user', type_='unique')
    op.drop_column('user', 'username')
    op.drop_table('favorites')
    op.drop_table('planet')
    op.drop_table('character')
    # ### end Alembic commands ###
