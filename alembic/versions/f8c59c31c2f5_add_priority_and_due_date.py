"""add priority and due date

Revision ID: f8c59c31c2f5
Revises: 9b0e07f8faa2
Create Date: 2026-06-11 08:10:42.925842

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f8c59c31c2f5'
down_revision: Union[str, Sequence[str], None] = '9b0e07f8faa2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    priority_enum = sa.Enum(
        'LOW',
        'MEDIUM',
        'HIGH',
        name='priorityenum'
    )

    status_enum = sa.Enum(
        'TODO',
        'IN_PROGRESS',
        'DONE',
        name='statusenum'
    )

    priority_enum.create(
        op.get_bind(),
        checkfirst=True
    )

    status_enum.create(
        op.get_bind(),
        checkfirst=True
    )

    op.add_column(
        'tasks',
        sa.Column(
            'priority',
            priority_enum,
            nullable=True
        )
    )

    op.add_column(
        'tasks',
        sa.Column(
            'due_date',
            sa.DateTime(),
            nullable=True
        )
    )



def downgrade() -> None:


    op.drop_column('tasks', 'due_date')
    op.drop_column('tasks', 'priority')

    sa.Enum(
        'LOW',
        'MEDIUM',
        'HIGH',
        name='priorityenum'
    ).drop(
        op.get_bind(),
        checkfirst=True
    )

    sa.Enum(
        'TODO',
        'IN_PROGRESS',
        'DONE',
        name='statusenum'
    ).drop(
        op.get_bind(),
        checkfirst=True
    )