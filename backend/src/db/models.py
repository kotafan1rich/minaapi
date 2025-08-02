from sqlalchemy import Column, DateTime, MetaData, func
from sqlalchemy.orm import declarative_base, declared_attr

POSTGRES_INDEXES_NAMING_CONVENTION = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}

metadata = MetaData(naming_convention=POSTGRES_INDEXES_NAMING_CONVENTION)

Base = declarative_base(
    metadata=metadata
)


class BaseModel(Base):
    __abstract__ = True

    time_created = Column(DateTime(), server_default=func.now())
    time_updated = Column(DateTime(), server_default=func.now(), onupdate=func.now())

    @declared_attr.directive
    def __tablename__(cls):
        # Получаем имя класса, преобразуем в нижний регистр и добавляем 's'
        return cls.__name__.lower() + 's'
