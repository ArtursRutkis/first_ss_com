from ss_scraper import cars_data, ssreq


def scrape(brand: str):
    """Scrapes uour sellected brand car from ss.com"""
    URLS = [
        f"https://www.ss.com/lv/transport/cars/{brand}/sell/",
        f"https://www.ss.com/lv/transport/cars/{brand}/sell/page2.html",
        f"https://www.ss.com/lv/transport/cars/{brand}/sell/page3.html",
        f"https://www.ss.com/lv/transport/cars/{brand}/sell/page4.html",
        f"https://www.ss.com/lv/transport/cars/{brand}/sell/page5.html",
    ]
    car_catalogue = []
    for link in URLS:
        try:
            list = ssreq(url=link)
            element = cars_data(list)
            car_catalogue.append(element)
        except ValueError:
            text = f"'error': 'No cars found for search criteria {brand}.'"
            print(text)
    return car_catalogue


def car_catalog(brand: str):
    car_cat = scrape(brand)
    data_base = []
    data_base2 = []
    for list in car_cat:
        for element in list:
            database_dict = {}
            database_dict["year"] = int(element[0])
            database_dict["model"] = element[1]
            x = element[2].replace(",", ".").replace(" ", "")
            # x = round(x,3)
            # x = format(float(x), ".3f")
            database_dict["price"] = x
            database_dict["engine"] = element[3]
            y = element[4].replace(" tūkst.", "000 km")
            database_dict["milage"] = y
            database_dict["url"] = "https://ss.com" + str(element[-1])
            data_base.append(database_dict)
            year = int(element[0])
            model = str(element[1])
            price = element[2].replace(",", "").replace(" ", "")
            engine_x = element[3].replace("H", "")
            engine_x = engine_x.replace("D", "")
            engine_x = engine_x.replace("E", "01.01")
            engine = float(engine_x)
            milage = (
                element[4].replace(" tūkst.", "000").replace(".", "").replace(",", "")
            )
            if milage == "-":
                milage = 0
            url = element[-1]
            data_base2.append(
                (year, str(model), int(price), float(engine), int(milage), url)
            )

    return data_base2


# schedule.every(3).minutes.do(scrape)

# while True:
#     schedule.run_pending()
#     time.sleep(1)
