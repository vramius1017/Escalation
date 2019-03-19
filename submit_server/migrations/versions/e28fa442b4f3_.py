"""empty message

Revision ID: e28fa442b4f3
Revises: d18508fd00d3
Create Date: 2019-03-18 17:57:49.614546

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e28fa442b4f3'
down_revision = 'd18508fd00d3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('training_run',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('dataset', sa.String(length=64), nullable=True),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('_rxn_M_inorganic', sa.Float(), nullable=True),
    sa.Column('_rxn_M_organic', sa.Float(), nullable=True),
    sa.Column('_out_crystalscore', sa.Integer(), nullable=True),
    sa.Column('inchikey', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('training_run')
    # ### end Alembic commands ###