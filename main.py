import requests
from bs4 import BeautifulSoup
import time
import schedule
import sqlite3

URLS = ["https://www.ss.com/lv/transport/cars/bmw/sell/"]

def bot(text):
    TELEGRAM_TOKEN = "6953171077:AAH3j5jHyHFg_OUDC6wj2ZvRpW9e3n9nY1U"
    BOT_USERNAME = "@BMW_sscom_bot"
    CHAT_ID = "-1002071459384"
    chat_message_text = 'https://api.telegram.org/bot' + TELEGRAM_TOKEN + '/sendMessage?chat_id=' + CHAT_ID + '&text=' + text
    requests.get(chat_message_text)


def sscomreq(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    table = soup.find("table", align="center")
    tr_table = table.find_all("tr")
    cars_table = []
    for car in tr_table:
        td = car.find_all('td')
        cars_table.append(td)
    clean_car_table = cars_table[1:61]

    behas = []
    for car in clean_car_table:
        model = car[3].text
        year = car[4].text
        price = car[7].text
        
        for link in car:
            link_end = link.find("a")
            if link_end:
                car_url = link_end['href']
                
        behas.append((year, model, price[0:-1], str(car_url)))

    conn = sqlite3.connect('behas.db')
    curs = conn.cursor()
    data_base_records = []
    query = """SELECT * FROM cars"""
    curs.execute(query)
    records = curs.fetchall()
    for record in records:
        data_base_records.append(record)

    for car in behas:
        if car not in data_base_records:
            print(f'car {car} not in data base\nAdding.....')
            curs.execute("INSERT OR IGNORE INTO cars VALUES (?, ?, ?, ?)", car)
            conn.commit()
            text = "Jauna beha tirgu!!! " + "www.ss.com/" + str(car[3])
            bot(text)
        else:
            print(f'Beha {car} already in data base')
    conn.close()


def scrape():
    for link in URLS:
        sscomreq(url=link)


schedule.every(2).minutes.do(scrape)

while True:
    schedule.run_pending()
    time.sleep(1)
