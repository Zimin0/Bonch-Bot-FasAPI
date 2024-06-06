"""Change update and delete modes to user model

Revision ID: 4a205fc8deff
Revises: ad05bcebee58
Create Date: 2024-06-06 22:45:01.346816

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4a205fc8deff'
down_revision = 'ad05bcebee58'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_settings_id', table_name='settings')
    op.drop_table('settings')
    op.drop_constraint('pc_sessions_tg_tag_fkey', 'pc_sessions', type_='foreignkey')
    op.create_foreign_key(None, 'pc_sessions', 'users', ['tg_tag'], ['tg_tag'], onupdate='CASCADE', ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'pc_sessions', type_='foreignkey')
    op.create_foreign_key('pc_sessions_tg_tag_fkey', 'pc_sessions', 'users', ['tg_tag'], ['tg_tag'])
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
