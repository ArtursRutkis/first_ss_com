import sqlalchemy.ext.declarative as _declarative
import sqlalchemy.orm as _orm

import dbsqlalchemy as _sql

DATABASE_URL = "postgresql://postgres:password@localhost:5432/fastapi_database"
engine = _sql.create_engine(DATABASE_URL)
SessionLocal = _orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = _declarative.declarative_base()
