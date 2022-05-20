import uuid

from geoalchemy2 import Geometry
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID


class Polygon(Base):
    __tablename__ = "polygons"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    project_id = Column(UUID(as_uuid=True), ForeignKey('projects.id'))
    geom = Column('geom', Geometry('POLYGON'), nullable=True)


class Customer(UUIDMixin, ActiveRecordMixin, Base):
    """Customer Account."""

    __tablename__ = 'customers'

    sf_account_id = Column(String, nullable=False, index=True)
    name = Column(String, nullable=False)
    account_type = Column(Enum(AccountTypeEnum, validate_strings=True), nullable=False)
    avatar = Column(String)
    plan = Column(String)
    point_of_contact_id = Column(UUID(as_uuid=True), ForeignKey('employees.id'))

    activated_at = Column(DateTime)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    discarded_at = Column(DateTime)
