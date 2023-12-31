"""addeded brand

Revision ID: 5788605c4d46
Revises: c5dea1b61959
Create Date: 2023-12-01 16:04:08.192939

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5788605c4d46'
down_revision = 'c5dea1b61959'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('review', schema=None) as batch_op:
        batch_op.add_column(sa.Column('brand', sa.String(length=64), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('review', schema=None) as batch_op:
        batch_op.drop_column('brand')

    # ### end Alembic commands ###
