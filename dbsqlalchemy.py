import sqlalchemy.orm as _orm
from sqlalchemy import (
    Column,
    Float,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
    text,
)
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.exc import SQLAlchemyError

from main import car_catalog

engine = create_engine("postgresql://postgres:password@localhost:5432/fastapi_database")

metadata = MetaData()


def create_table_for_brand(brand: str):
    cars = Table(
        f"{brand}",
        metadata,
        Column("year", Integer),
        Column("model", String),
        Column("price", Integer),
        Column("engine", Float),
        Column("milage", Integer),
        Column("url", String, primary_key=True),
    )
    return cars


metadata.create_all(engine)


def insert_data_in_db(rows, cars):
    conn = engine.connect()
    stmt = (
        insert(cars)
        .values(
            [
                {
                    "year": year,
                    "model": model,
                    "price": price,
                    "engine": engine,
                    "milage": milage,
                    "url": url,
                }
                for year, model, price, engine, milage, url in rows
            ]
        )
        .on_conflict_do_nothing(index_elements=["url"])
    )

    with engine.begin() as conn:
        conn.execute(stmt)
        conn.commit()
        conn.close()


SessionLocal = _orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_for_table(brand):
    conn = engine.connect()
    table = Table(brand, metadata)
    stop = True
    try:
        query = text(f"select * from {table}")
        conn.execute(query).fetchone()
        conn.commit()
        stop = False
        conn.close()
    except SQLAlchemyError as e:
        print(e)
        stop = True

    return stop


def get_from_db(
    brand,
    year_from,
    year_till,
    price_from,
    price_till,
    milage_from,
    milage_till,
    motor,
):
    conn = engine.connect()

    table = Table(brand, metadata)
    if motor is None:
        query = text(
            f"""SELECT * FROM {table} WHERE year BETWEEN {year_from} AND {year_till} AND price BETWEEN {price_from} AND {price_till} AND milage BETWEEN {milage_from} AND {milage_till}"""
        )
    else:
        query = text(
            f"""SELECT * FROM {table} WHERE year BETWEEN {year_from} AND {year_till} AND price BETWEEN {price_from} AND {price_till} AND milage BETWEEN {milage_from} AND {milage_till} AND engine = {motor}"""
        )
    results = conn.execute(query).fetchall()
    conn.commit()
    dict_result = []
    for result in results:
        dict_result.append(result._asdict())
    conn.close()
    if len(dict_result) < 1:
        return {"message": "there is 0 cars by your criteria"}
    return dict_result
