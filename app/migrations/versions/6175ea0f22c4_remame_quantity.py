"""remame quantity

Revision ID: 6175ea0f22c4
Revises: c911c9d7b283
Create Date: 2023-11-14 15:45:57.492630

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '6175ea0f22c4'
down_revision: Union[str, None] = 'c911c9d7b283'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('hotels', sa.Column('rooms_quantity', sa.Integer(), nullable=False))
    op.drop_column('hotels', 'room_quantity')
    op.add_column('rooms', sa.Column('quantity', sa.Integer(), nullable=False))
    op.drop_column('rooms', 'rooms_quantity')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('rooms', sa.Column('rooms_quantity', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_column('rooms', 'quantity')
    op.add_column('hotels', sa.Column('room_quantity', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_column('hotels', 'rooms_quantity')
    # ### end Alembic commands ###