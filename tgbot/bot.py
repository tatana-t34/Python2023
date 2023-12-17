import requests
from bs4 import BeautifulSoup
import datetime
import data_base as data_base
import sqlite3
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

data_base.create_table()

headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.686 YaBrowser/23.9.5.686 Yowser/2.5 Safari/537.36"
            }
count_pages = 2 
for URL in [("https://bits.media/news/?nav_feed=page-" + str(i)) for i in range(1, count_pages + 1)]:
    page = requests.get(url=URL, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    news = soup.find_all("div", class_="news-item")
    for new in news:
        date = datetime.datetime.now()
        #current_date дате сегодня, можно поменять на другую дату
        current_date = str(date.day) + '.' + str(date.month) + '.' + str(date.year)
        for i in range(1, 10):
            if str(date.month) == str(i):
                current_date = str(date.day) + '.' + "0" + str(date.month) + '.' + str(date.year)
            if str(date.day) == str(i):
                current_date = "0" + current_date
        if (new.find("span", class_="news-date").text.strip()) == current_date:
            news_title = new.find("a", class_="news-name").text.strip()
            news_content = new.find("div", class_="news-text").text.strip()
            news_date = new.find("span", class_="news-date").text.strip()
            news_url = f'https://bits.media{new.find("a", class_="news-name", href=True)["href"].strip()}'
            try:
                if data_base.check_news(news_title) == False:
                    data_base.insert_news(news_title, news_content, news_date, news_url)
            except Exception as ex:
                continue
        else:
            break

database = sqlite3.connect('news_db.db')
cursor = database.cursor()
bot = Bot(token='6704686661:AAHra418RVGdH7M61keQmT-Cfje3yVocab8')
dp = Dispatcher()

@dp.message(Command('show_table'))
async def show_table(message: types.Message):
    cursor.execute('SELECT * FROM news')
    data = cursor.fetchall()

    response = ""
    for row in data:
        response += " | ".join(str(cell) for cell in row) + "\n"
    if len(response) > 4096:
        for x in range(0, len(response), 4096):
            await message.answer(response[x:x+4096])
    else:
        await message.answer(response)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())