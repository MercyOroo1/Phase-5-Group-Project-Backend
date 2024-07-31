"""change to agent  table

Revision ID: 6f3eae50cd6f
Revises: 757b211643ae
Create Date: 2024-07-31 14:35:05.062894

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6f3eae50cd6f'
down_revision = '757b211643ae'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('properties', schema=None) as batch_op:
        batch_op.alter_column('agent_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('properties', schema=None) as batch_op:
        batch_op.alter_column('agent_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###
