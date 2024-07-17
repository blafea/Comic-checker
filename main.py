# -- coding: utf-8 --
from telegram.ext import CommandHandler, ApplicationBuilder
import datetime
import comic_crawler
import json
import requests
import bs4
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.environ["TELEGRAM_TOKEN"]


async def hello(update, context):
    await update.message.reply_text('hello, {}'.format(
        update.message.from_user.first_name))


async def list(update, context):
    with open("./database.json", 'r') as f:
        data = json.loads(f.read())
    for key, value in data.items():
        await update.message.reply_text(f'{key}\n{value}')


async def add(update, context):
    try:
        new = update.message.text[5:].split(" ")
        with open("./database.json", 'r') as f:
            data = json.loads(f.read())
        with open("./database.json", 'w') as f:
            data.update({new[0]: new[1]})
            json.dump(data, f)
            print(data)
        await update.message.reply_text(f'{new[0]} 新增成功')
    except:
        await update.message.reply_text('新增失敗')


async def delete(update, context):
    new = update.message.text[5:]
    try:
        with open("./database.json", 'r') as f:
            data = json.loads(f.read())
        with open("./database.json", 'w') as f:
            data.pop(new)
            json.dump(data, f)
            print(data)
        await update.message.reply_text(f'{new} 刪除成功')
    except:
        await update.message.reply_text('刪除失敗')


async def check_loop(update):
    send = False
    with open("database.json", "r") as f:
        data = json.loads(f.read())
    for key, value in data.items():
        print(key)
        if comic_crawler.check(value):
            await update.bot.send_message(chat_id="843970308",
                                          text="{} 已更新\n{}".format(key, value))
            send = True
    if not send:
        await update.bot.send_message(chat_id="843970308", text="沒有漫畫更新")


async def check_now(update, context):
    send = False
    with open("database.json", "r") as f:
        data = json.loads(f.read())
    await update.message.reply_text(f"開始檢查 {len(data)} 部漫畫")
    for key, value in data.items():
        print(key)
        if comic_crawler.check(value):
            await update.message.reply_text(f"{key} 已更新\n{value}")
            send = True
    if not send:
        await update.message.reply_text("沒有漫畫更新")


async def check_3090(update):
    URL = "https://www.ptt.cc/bbs/HardwareSale/index.html"
    response = requests.get(URL)

    soup = bs4.BeautifulSoup(response.text, "html.parser")
    header = soup.find_all("div", class_="title")

    for h in header:
        if ("3090" in h.text) and ("賣" in h.text.replace("賣貨便", "")):
            await update.bot.send_message(chat_id="843970308", text="find 3090")
        else:
            print("no")


if __name__ == "__main__":
    application = ApplicationBuilder().token(TOKEN).build()
    j = application.job_queue
    j.run_repeating(check_loop,
                    interval=datetime.timedelta(hours=12),
                    first=datetime.time(hour=15, minute=59))
    # j.run_repeating(check_3090,
    #                 interval=datetime.timedelta(minutes=5),
    #                 first=datetime.time())
    application.add_handler(CommandHandler('hello', hello))
    application.add_handler(CommandHandler('add', add))
    application.add_handler(CommandHandler('del', delete))
    application.add_handler(CommandHandler('list', list))
    application.add_handler(CommandHandler('check', check_now))

    application.run_polling()
