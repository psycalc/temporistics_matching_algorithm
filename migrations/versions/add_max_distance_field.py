"""add max_distance field

Revision ID: add_max_distance_field
Revises: 
Create Date: 2023-06-15 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_max_distance_field'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Додаємо нове поле max_distance в таблицю users
    op.add_column('users', sa.Column('max_distance', sa.Float(), nullable=True, server_default='50.0'))


def downgrade():
    # Видаляємо поле max_distance з таблиці users
    op.drop_column('users', 'max_distance') 