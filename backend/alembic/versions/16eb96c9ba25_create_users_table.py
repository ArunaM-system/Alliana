"""create users table

Revision ID: 16eb96c9ba25
Revises: 
Create Date: 2025-07-22 21:39:55.946998

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '16eb96c9ba25'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False, unique=True),
    )

    # Insert initial users
    op.execute(
        """
        INSERT INTO users (name, email) VALUES
        ('Alice', 'alice@example.com'),
        ('Bob', 'bob@example.com'),
        ('Charlie', 'charlie@example.com'),
        ('Diana', 'diana@example.com'),
        ('Eve', 'eve@example.com'),
        ('Frank', 'frank@example.com'),
        ('Grace', 'grace@example.com'),
        ('Heidi', 'heidi@example.com'),
        ('Ivan', 'ivan@example.com'),
        ('Judy', 'judy@example.com')
        """
    )

def downgrade() -> None:
    op.drop_table('users')
