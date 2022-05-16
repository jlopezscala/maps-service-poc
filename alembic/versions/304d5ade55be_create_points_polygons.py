"""create_points_polygons

Revision ID: 304d5ade55be
Revises: b6e0925ba7f2
Create Date: 2022-05-15 21:03:52.702839

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy import ForeignKey

# revision identifiers, used by Alembic.
revision = '304d5ade55be'
down_revision = 'b6e0925ba7f2'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'pointsxpolygon',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('polygon_id', postgresql.UUID(as_uuid=True), ForeignKey('polygons.id')),
        sa.Column('x', sa.Unicode(200)),
        sa.Column('y', sa.Unicode(200)),
    )


def downgrade():
    op.drop_table('polygons')
