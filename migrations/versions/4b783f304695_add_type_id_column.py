"""Add type_id column

Revision ID: 4b783f304695
Revises: 412f969c6300
Create Date: 2024-12-07 06:02:36.412654

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4b783f304695'
down_revision = '412f969c6300'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('type_id', sa.Integer(), nullable=True))
    op.alter_column('user', 'username',
               existing_type=sa.VARCHAR(length=64),
               type_=sa.String(length=80),
               existing_nullable=False)
    op.alter_column('user', 'password_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=False)
    op.create_foreign_key(None, 'user', 'user_type', ['type_id'], ['id'])
    op.alter_column('user_type', 'typology_name',
               existing_type=sa.VARCHAR(length=64),
               type_=sa.String(length=50),
               existing_nullable=False)
    op.alter_column('user_type', 'type_value',
               existing_type=sa.VARCHAR(length=64),
               type_=sa.String(length=50),
               existing_nullable=False)
    op.drop_constraint('user_type_user_id_fkey', 'user_type', type_='foreignkey')
    op.drop_column('user_type', 'user_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_type', sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('user_type_user_id_fkey', 'user_type', 'user', ['user_id'], ['id'])
    op.alter_column('user_type', 'type_value',
               existing_type=sa.String(length=50),
               type_=sa.VARCHAR(length=64),
               existing_nullable=False)
    op.alter_column('user_type', 'typology_name',
               existing_type=sa.String(length=50),
               type_=sa.VARCHAR(length=64),
               existing_nullable=False)
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.alter_column('user', 'password_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=True)
    op.alter_column('user', 'username',
               existing_type=sa.String(length=80),
               type_=sa.VARCHAR(length=64),
               existing_nullable=False)
    op.drop_column('user', 'type_id')
    # ### end Alembic commands ###