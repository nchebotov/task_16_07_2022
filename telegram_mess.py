import pandas as pd
import time, asyncio
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage


API_KEY = ''

#bot = telebot.TeleBot(API_KEY)
bot = Bot(token=API_KEY)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


#   Функционал нахождения номеров заказов, у которых истек срок поставки, и отправка уведомлений в Telegram
#   Так же можно реализовать напрямую из Google Sheets получать данные
def date_order():
    yesterday = time.strftime('%d.%m.%Y', time.gmtime(time.time() - 86400))
    with open('records/data_csv.csv', 'r+') as f:
        orders = pd.read_csv(f, sep=';', index_col='number')
        filter_large = orders.query(f"delivery_date == '{yesterday}'")
        print(filter_large)
        order_number = filter_large[['order_number']]
        print(order_number)
        f.close()
        return order_number


#   Функционал, который отправляет уведомления об истечении срока определенным людям из списка all_user.
#   ('723232562'- testing id)
async def on_start(_):
    all_user = ['000000000']
    for user_id in all_user:
        await bot.send_message(chat_id=user_id, text=f"Здравствуйте. Сегодня истек срок поставки у данного(-ых)"
                                                     f" заказа(-ов) 😔: \n"
                                                     f"'{date_order().order_number}'.")
        await asyncio.sleep(1)


if __name__ == '__main__':
    date_order()
    executor.start_polling(dp, skip_updates=True, on_startup=on_start)


