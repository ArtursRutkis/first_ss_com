import sqlite3

from fastapi import FastAPI, HTTPException

from dbsqlalchemy import (
    check_for_table,
    create_table_for_brand,
    engine,
    get_from_db,
    insert_data_in_db,
    metadata,
)
from main import car_catalog
from telegram_bot import bot_send_message

car_brands = [
    "alfa Romeo",
    "audi",
    "bmw",
    "chevrolet",
    "chrysler",
    "citroen",
    "dacia",
    "dodge",
    "fiat",
    "ford",
    "honda",
    "hyndai",
    "infiniti",
    "jaguar",
    "jeep",
    "kia",
    "lancia",
    "land rover",
    "lexus",
    "mazda",
    "mercedes",
    "mini",
    "mitsubishi",
    "nissan",
    "opel",
    "peugeot",
    "porsche",
    "renault",
    "saab",
    "seat",
    "skoda",
    "smart",
    "subaru",
    "suzuki",
    "toyota",
    "volkswagen",
    "volvo",
    "gaz",
    "uaz",
    "vaz",
    "citas markas",
]
app = FastAPI()


@app.get("/")
def root():
    return {"Hello": "Scraper"}


@app.get(
    "/all/search",
    description="Insert Car Brand, optional: '(year from, year till, price_from, price_till, milage_from, milage_till, engine(accurate, for electric:01.01)",
)
async def read_items_params(
    brand: str,
    year_from: int | None = 0,
    year_till: int | None = 999999,
    price_from: int | None = 0,
    price_till: int | None = 999999,
    milage_from: int | None = 0,
    milage_till: int | None = 999999,
    engine: float | None = None,
):
    """Append requested brand to catalog"""

    if brand.lower() not in car_brands:
        raise HTTPException(
            status_code=400,
            detail={"error": "Incorect car brand criteria.", "kays": car_brands},
        )

    create_database(brand)
    cars = car_catalog(brand)
    insert_in_db(brand, cars)
    conn = sqlite3.connect("cars_database.db")

    conn.row_factory = sqlite3.Row
    curs = conn.cursor()
    query = f"""SELECT * FROM {brand} WHERE year BETWEEN {year_from} AND {year_till} AND price BETWEEN {price_from} AND {price_till} AND milage BETWEEN {milage_from} AND {milage_till}"""
    if engine:
        query += f" AND engine = {engine}"
    curs.execute(query)
    records = [dict(row) for row in curs.fetchall()]
    query2 = f"""DROP TABLE {brand}"""
    curs.execute(query2)
    conn.close()
    for record in records:
        record["url"] = "www.ss.com" + str(record["url"])
        # bot_send_message(f'{brand} pec taviem kriterijiem {record["url"]}')
    if len(records) < 1:
        raise HTTPException(
            status_code=400, detail={"error": "No cars found for search criteria."}
        )
    return {brand: records}

    # else:
    #     query = f"""SELECT * FROM {brand} WHERE year BETWEEN {year_from} AND {year_till} AND price BETWEEN {price_from} AND {price_till} AND milage BETWEEN {milage_from} AND {milage_till}  """
    #     curs.execute(query)
    #     records = [dict(row) for row in curs.fetchall()]
    #     query2 = f"""DROP TABLE {brand}"""
    #     curs.execute(query2)
    #     conn.close()
    #     for record in records:
    #         record["url"] = "www.ss.com" + str(record["url"])
    #         # bot_send_message(f'{brand} pec taviem kriterijiem {record["url"]}')
    #     if len(records) < 1:
    #         raise HTTPException(
    #             status_code=400, detail={"error": "No cars found for search criteria."}
    #         )
    #     return {brand: records}


@app.get("/all/{request}", description="Insert Car Brand")
async def read_items(request: str):
    if request.lower() not in car_brands:
        raise HTTPException(
            status_code=400, detail={"error": "Incorect car brand criteria."}
        )

    results_all = car_catalog(request)
    return results_all


################################################################
@app.post("/create", description="I will scrape selected brand from ss.com")
def create_records_in_db(request: str):
    if request.lower() not in car_brands:
        raise HTTPException(
            status_code=400, detail={"error": "Incorect car brand criteria."}
        )

    rows = car_catalog(request)
    cars = create_table_for_brand(request)
    metadata.create_all(engine)
    insert_data_in_db(rows, cars)

    # We scrape from ss

    # We instert into database
    return {"statuss": "ok", "message": "data added"}


###################################################################


@app.get(
    "/cars",
    description="Insert Car Brand, optional: '(year from, year till, price_from, price_till, milage_from, milage_till, engine(accurate, for electric:01.01)",
)
async def return_cars(
    brand: str,
    year_from: int | None = 0,
    year_till: int | None = 999999,
    price_from: int | None = 0,
    price_till: int | None = 999999,
    milage_from: int | None = 0,
    milage_till: int | None = 999999,
    motor: float | None = None,
):
    if brand.lower() not in car_brands:
        raise HTTPException(
            status_code=400, detail={"error": "Incorect car brand criteria."}
        )
    if check_for_table(brand=brand) is False:

        return get_from_db(
            brand,
            year_from=year_from,
            year_till=year_till,
            price_from=price_from,
            price_till=price_till,
            milage_from=milage_from,
            milage_till=milage_till,
            motor=motor,
        )
    else:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Selected brand not in our data base, please do post request first!"
            },
        )


########################################################################
# conn = engine.connect()
# # stmt = text(f"SELECT * FROM {brand}")
# stmt = Table(brand, metadata).select()
# # Read from database
# results = conn.execute(stmt).fetchall()
# conn.commit()
# dict_result = []
# for result in results:
#     print(type(result))
#     # dict_result.append(dict(result))

#     dict_result.append(result._asdict())
# # print(dict_result)
# conn.close()
# return dict_result


# Endpoint:
#     - Noskrape un ieviedo datubaze un atgriez message ka ir ok
#     - Nolasa no datubazes balstoties uz kriterijiem
