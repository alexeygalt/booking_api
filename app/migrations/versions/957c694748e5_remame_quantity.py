"""remame quantity

Revision ID: 957c694748e5
Revises: 568a174984f0
Create Date: 2023-11-14 15:43:42.169602

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '957c694748e5'
down_revision: Union[str, None] = '568a174984f0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('rooms', sa.Column('rooms_quantity', sa.Integer(), nullable=False))
    op.drop_column('rooms', 'quantity')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('rooms', sa.Column('quantity', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_column('rooms', 'rooms_quantity')
    # ### end Alembic commands ###