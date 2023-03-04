# -- coding: utf-8 --
from telegram.ext import Updater, CommandHandler
import datetime
import comic_crawler
import json
import keep_alive

def hello(update, context):
    update.message.reply_text('hello, {}'.format(update.message.from_user.first_name))

def list(update, context):
    with open("./database.json", 'r') as f:
        data = json.loads(f.read())
    for key, value in data.items():
        update.message.reply_text(f'{key}\n{value}')

def add(update, context):
    try:
        new = update.message.text[5:].split(" ")
        with open("./database.json", 'r') as f:
            data = json.loads(f.read())
        with open("./database.json", 'w') as f:
            data.update({new[0]:new[1]})
            json.dump(data, f)
            print(data)
        update.message.reply_text(f'{new[0]} 新增成功')
    except:
        update.message.reply_text('新增失敗')

def delete(update, context):
    new = update.message.text[5:]
    try:
        with open("./database.json", 'r') as f:
            data = json.loads(f.read())
        with open("./database.json", 'w') as f:
            data.pop(new)
            json.dump(data, f)
            print(data)
        update.message.reply_text(f'{new} 刪除成功')
    except:
        update.message.reply_text('刪除失敗')

def check_loop(update):
    send = False
    with open("database.json", "r") as f:
        data = json.loads(f.read())
    for key, value in data.items():
        print(key)
        if comic_crawler.check(value):
            update.bot.send_message(chat_id="843970308", text="{} 已更新\n{}".format(key, value))
            send = True
    if not send:
        update.bot.send_message(chat_id="843970308", text="沒有漫畫更新")

def check_now(update, context):
    send = False
    with open("database.json", "r") as f:
        data = json.loads(f.read())
    update.message.reply_text(f"開始檢查 {len(data)} 部漫畫")
    for key, value in data.items():
        print(key)
        if comic_crawler.check(value):
            update.message.reply_text(f"{key} 已更新\n{value}")
            send = True
    if not send:
        update.message.reply_text("沒有漫畫更新")

updater = Updater('6269578873:AAE6exmJI8M74lgEJD1S-LOOQhWSXE8OEsc')
j = updater.job_queue
# j.run_repeating(check, interval=10)
j.run_repeating(check_loop, interval=datetime.timedelta(days=1), first=datetime.time(hour=15, minute=59))
updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(CommandHandler('add', add))
updater.dispatcher.add_handler(CommandHandler('del', delete))
updater.dispatcher.add_handler(CommandHandler('list', list))
updater.dispatcher.add_handler(CommandHandler('check', check_now))

if __name__ == "__main__":
    keep_alive.keep_alive()
    updater.start_polling()
    updater.idle()
    updater.stop()

# def hello(bot, update):
#     update.message.reply_text('hello, {}'.format(update.message.from_user.first_name))

# def add(bot, update):
#     new = update.message.text[5:].split(" ")
#     with open("./database.json", 'r+') as f:
#         data = json.loads(f.read())
#         data.update({new[0]:new[1]})
#         json.dump(data)
#         print(data)

# def check(bot, update):
#     while True:
#         with open("database.json", "r") as f:
#             data = json.loads(f.read())
#         for key, value in data:
#             if comic_crawler.check(value):
#                 update.message.reply_text("{}:{}".format(key, value))
#         time.sleep(10)
    

# updater = Updater('6269578873:AAE6exmJI8M74lgEJD1S-LOOQhWSXE8OEsc')

# updater.dispatcher.add_handler(CommandHandler('hello', hello))
# updater.dispatcher.add_handler(CommandHandler('add', add))
# updater.dispatcher.add_handler(CommandHandler('check', check))

# updater.start_polling()
# updater.idle()