"""main

Revision ID: a045316e0fdd
Revises: 
Create Date: 2025-04-04 21:55:56.948678

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a045316e0fdd'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('account',
    sa.Column('telegram_id', sa.String(), autoincrement=False, nullable=False),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('telephone', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('telegram_id')
    )
    op.create_table('component',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('group', sa.String(), nullable=True),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('hide', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('entry',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('client_id', sa.String(), nullable=True),
    sa.Column('create_at', sa.DateTime(), nullable=True),
    sa.Column('completed_at', sa.DateTime(), nullable=True),
    sa.Column('completed', sa.Boolean(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('contact', sa.String(), nullable=True),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['client_id'], ['account.telegram_id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('entry_component',
    sa.Column('entry_id', sa.Integer(), nullable=False),
    sa.Column('component_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['component_id'], ['component.id'], ),
    sa.ForeignKeyConstraint(['entry_id'], ['entry.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('entry_id', 'component_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('entry_component')
    op.drop_table('entry')
    op.drop_table('component')
    op.drop_table('account')
    # ### end Alembic commands ###
