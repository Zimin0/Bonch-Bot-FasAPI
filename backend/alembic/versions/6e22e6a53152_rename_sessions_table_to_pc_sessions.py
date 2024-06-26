"""Rename Sessions table to pc_Sessions

Revision ID: 6e22e6a53152
Revises: 33f2043ff3db
Create Date: 2024-05-30 22:21:54.145108

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6e22e6a53152'
down_revision = '33f2043ff3db'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_settings_id', table_name='settings')
    op.drop_table('settings')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
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
