import uuid
from datetime import datetime

from geoalchemy2 import Geometry, functions
from sqlalchemy import MetaData, Table, Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapper, relationship, column_property

from src.domain import model

metadata = MetaData()

projects = Table(
    "projects",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("name", String(255)),
    Column("description", String(255), nullable=False),
    Column("updated_at", DateTime, nullable=False, default=datetime.utcnow),
    Column("created_at", DateTime, nullable=False, default=datetime.utcnow),
)

polygons = Table(
    "polygons",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("project_id", ForeignKey("projects.id")),
    Column("name", String(255), nullable=False),
    Column("description", String(255), nullable=True),
    Column("geom", Geometry("POLYGON"), nullable=True),
    Column("updated_at", DateTime, nullable=False, default=datetime.utcnow),
    Column("created_at", DateTime, nullable=False, default=datetime.utcnow),
)


def start_mappers():
    polygon_mapper = mapper(model.Polygon, polygons,
                            properties={"geom_json": column_property(functions.ST_AsGeoJSON(polygons.c.geom))})
    mapper(model.Project,
           projects,
           properties={"features": relationship(
               polygon_mapper,
               cascade="all")})
