"""Time mixin

Revision ID: b1c96607a3a7
Revises: 0d9ee9a3bf47
Create Date: 2024-06-17 17:37:29.309781

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b1c96607a3a7'
down_revision = '0d9ee9a3bf47'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bank_accounts', sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.add_column('bank_accounts', sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.add_column('customers', sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.add_column('customers', sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.add_column('transactions', sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.add_column('transactions', sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('transactions', 'created_at')
    op.drop_column('transactions', 'updated_at')
    op.drop_column('customers', 'created_at')
    op.drop_column('customers', 'updated_at')
    op.drop_column('bank_accounts', 'created_at')
    op.drop_column('bank_accounts', 'updated_at')
    # ### end Alembic commands ###
