import time
import requests
import telebot
from bs4 import BeautifulSoup

TOKEN = ""
storage_cars = []
URL = "https://blackterminal.com/news?hl=ru"
HEADERS = {
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Mobile Safari/537.36",
    'accept': "*/*"}


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    time.sleep(3)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all(class_='media-body news-body')
    items_1 = soup.find_all(class_='col-md-6' > 'data-key')
    cars = []
    for item in items:
        car = {
            'title': item.find('div', class_='news-text').get_text(strip=True),
            'link': item.find('a').get_text('href')
        }
        if car['link'] not in map(lambda storage_car: storage_car['link'], storage_cars):
            return cars


def publish(cars):
    if len(cars) == 0:
        return

    bot = telebot.TeleBot(TOKEN)

    @bot.message_handler(content_types=['text'])
    def news(message):
        bot.send_message(message.chat.id, cars)

        bot.polling()
        news()


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        cars = get_content(html.text)
        storage_cars.extend(cars)
        publish(cars)
    else:
        print('Error')


if __name__ == '__main__':
    while True:
        parse()
        time.sleep(300)