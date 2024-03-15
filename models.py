import database as _database
import dbsqlalchemy as _sql


class Car(_database.Base):
    __tablename__ = "cars"

    year = _sql.Column(_sql.Integer, index=True)
    model = _sql.Column(_sql.String, index=True)
    price = _sql.Column(_sql.Integer, index=True)
    engine = _sql.Column(_sql.Float, index=True)
    milage = _sql.Column(_sql.Integer, index=True)
    url = _sql.Column(_sql.String, primary_key=True, index=True)
