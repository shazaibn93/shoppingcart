"""empty message

Revision ID: 33810eaed8d8
Revises: 08ee666c4181
Create Date: 2022-02-21 05:57:26.686563

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '33810eaed8d8'
down_revision = '08ee666c4181'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('cart', 'item_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.add_column('item', sa.Column('quantity', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('item', 'quantity')
    op.alter_column('cart', 'item_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
