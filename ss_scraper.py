import requests
from bs4 import BeautifulSoup


def ssreq(url: str):
    """Gets raw car data from SS.COM and returns raw list [clean_car_table]"""
    r = requests.get(url)

    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    table = soup.find("table", cellpadding="2")

    # align="center"

    tr_table = table.find_all("tr")

    cars_table = []
    for car in tr_table:
        td = car.find_all("td")
        cars_table.append(td)
    clean_car_table = cars_table[1:-1]

    return clean_car_table


def cars_data(ssreq: list):
    "returns specific data"

    behas = []
    behas2 = []
    for carx in ssreq:
        cars_dict = {}
        model = carx[3].text
        year = carx[4].text
        price = carx[7].text
        engine = carx[5].text
        milage = carx[6].text
        cars_dict["model"] = carx[3].text
        cars_dict["year"] = carx[4].text
        cars_dict["price"] = carx[7].text
        cars_dict["engine"] = carx[5].text
        cars_dict["milage"] = carx[6].text

        for link in carx:
            link_end = link.find("a")
            if link_end:
                car_url = link_end["href"]
                cars_dict["url"] = link_end["href"]

        #         behas2.append(cars_dict)
        behas.append((int(year), model, price[0:-1], engine, milage, str(car_url)))

    return behas


# x = ssreq("https://www.ss.com/lv/transport/cars/bmw/sell/")

# print(cars_data(x))
