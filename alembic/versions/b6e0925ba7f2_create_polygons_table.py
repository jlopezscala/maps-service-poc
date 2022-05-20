"""create_polygons_table

Revision ID: b6e0925ba7f2
Revises: 8f25b4c94aa7
Create Date: 2022-05-15 20:30:18.204673

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import ForeignKey
from sqlalchemy.dialects import postgresql
from geoalchemy2.types import Geometry

# revision identifiers, used by Alembic.
revision = 'b6e0925ba7f2'
down_revision = '8f25b4c94aa7'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'polygons',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('description', sa.String(255), nullable=True),
        sa.Column('project_id', postgresql.UUID(as_uuid=True), ForeignKey('projects.id', ondelete='CASCADE')),
        sa.Column('geom', Geometry('POLYGON')),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.current_timestamp()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.current_timestamp())
    )


def downgrade():
    op.drop_table('polygons')
