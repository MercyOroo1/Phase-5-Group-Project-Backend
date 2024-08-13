"""empty message

Revision ID: 4755eade70b3
Revises: f8dd17b53bc2
Create Date: 2024-08-13 22:54:16.081324

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4755eade70b3'
down_revision = 'f8dd17b53bc2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_payment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('total_installments', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_payment', schema=None) as batch_op:
        batch_op.drop_column('total_installments')

    # ### end Alembic commands ###
