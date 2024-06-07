"""Add column avatar to user model

Revision ID: f8e08c04bd76
Revises: 4a205fc8deff
Create Date: 2024-06-07 20:23:08.696617

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f8e08c04bd76'
down_revision = '4a205fc8deff'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_settings_id', table_name='settings')
    op.drop_table('settings')
    op.add_column('users', sa.Column('avatar', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'avatar')
    op.create_table('settings',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('slug', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('value', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='settings_pkey'),
    sa.UniqueConstraint('slug', name='settings_slug_key')
    )
    op.create_index('ix_settings_id', 'settings', ['id'], unique=False)
    # ### end Alembic commands ###
