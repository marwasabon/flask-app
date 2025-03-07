"""Unknown column 'claim_id 

Revision ID: ea1aa023cf1a
Revises: 03b12f75271e
Create Date: 2024-07-07 04:41:40.509028

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ea1aa023cf1a'
down_revision = '03b12f75271e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('matches', schema=None) as batch_op:
        batch_op.add_column(sa.Column('claim_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'claims', ['claim_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('matches', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('claim_id')

    # ### end Alembic commands ###
