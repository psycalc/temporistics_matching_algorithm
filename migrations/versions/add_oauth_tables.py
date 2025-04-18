"""add oauth tables

Revision ID: add_oauth_tables
Revises: add_oauth_fields
Create Date: 2023-06-16 11:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'add_oauth_tables'
down_revision = 'add_oauth_fields'
branch_labels = None
depends_on = None


def upgrade():
    # Створюємо таблицю для GoogleOAuth
    op.create_table(
        'google_oauth',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('token', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('provider', sa.String(length=50), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('profile_id', sa.String(length=256), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Створюємо таблицю для GitHubOAuth
    op.create_table(
        'github_oauth',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('token', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('provider', sa.String(length=50), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('login', sa.String(length=256), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('github_oauth')
    op.drop_table('google_oauth') 