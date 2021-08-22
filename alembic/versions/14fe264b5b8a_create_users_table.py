"""create users table

Revision ID: 14fe264b5b8a
Revises: 
Create Date: 2021-08-21 11:35:40.915764

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '14fe264b5b8a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'user_auth',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('login', sa.Integer, nullable=False),
        sa.Column('password', sa.String(10), nullable=False),
        sa.Column('username', sa.String(255), nullable=False),
        sa.Column('last_name', sa.String(150), nullable=True),
        sa.Column('first_name', sa.String(150), nullable=True),
        sa.Column('last_password', sa.String(10), nullable=False),
        sa.Column('last_active', sa.DateTime, nullable=False),
        sa.Column('date_joined', sa.DateTime, nullable=False),
        sa.Column('language', sa.String(32)),
        sa.Column('balance', sa.Float, nullable=False),
        sa.Column('ip_address', sa.String(15), nullable=True))

    op.create_table(
        'admin_auth',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('login', sa.String(255), nullable=False),
        sa.Column('password', sa.String(255), nullable=False))

    op.create_table(
        'attack_data',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('created', sa.DateTime, nullable=False),
        sa.Column('status', sa.String(50), nullable=False),
        sa.Column('last_phone', sa.String(50), nullable=True),
        sa.Column('last_created', sa.String(50), nullable=True)),

    op.create_table(
        'activate_orders',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('created', sa.DateTime, nullable=False),
        sa.Column('service', sa.String(255), nullable=False), 
        sa.Column('price', sa.Float, nullable=False))

def downgrade():
    op.drop_table('user_auth')
    op.drop_tabel('admin_auth')
