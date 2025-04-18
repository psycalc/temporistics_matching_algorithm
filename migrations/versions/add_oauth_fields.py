"""add oauth fields

Revision ID: add_oauth_fields
Revises: add_max_distance_field
Create Date: 2023-06-16 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_oauth_fields'
down_revision = 'add_max_distance_field'
branch_labels = None
depends_on = None


def upgrade():
    # Додаємо поля для OAuth
    op.add_column('users', sa.Column('google_id', sa.String(256), nullable=True, unique=True))
    op.add_column('users', sa.Column('github_id', sa.String(256), nullable=True, unique=True))
    op.add_column('users', sa.Column('avatar_url', sa.String(512), nullable=True))
    
    # Змінюємо password_hash на nullable
    op.alter_column('users', 'password_hash', existing_type=sa.String(128), nullable=True)


def downgrade():
    # Видаляємо поля OAuth
    op.drop_column('users', 'google_id')
    op.drop_column('users', 'github_id')
    op.drop_column('users', 'avatar_url')
    
    # Повертаємо password_hash як not nullable
    op.alter_column('users', 'password_hash', existing_type=sa.String(128), nullable=False) 