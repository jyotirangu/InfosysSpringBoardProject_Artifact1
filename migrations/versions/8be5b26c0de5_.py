"""empty message

Revision ID: 8be5b26c0de5
Revises: bcc437aeb750
Create Date: 2024-12-24 00:41:17.007422

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8be5b26c0de5'
down_revision = 'bcc437aeb750'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.String(length=300),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=sa.String(length=300),
               type_=sa.VARCHAR(length=255),
               existing_nullable=False)

    # ### end Alembic commands ###
