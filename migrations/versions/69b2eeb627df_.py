"""empty message

Revision ID: 69b2eeb627df
Revises: 0ce8c57944ac
Create Date: 2024-12-13 18:08:11.696219

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '69b2eeb627df'
down_revision = '0ce8c57944ac'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('isVerified', sa.String(length=20), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('isVerified')

    # ### end Alembic commands ###