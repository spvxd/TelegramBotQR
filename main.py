from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import pyqrcode as pq
import os

token_path = open('token.txt')
token = token_path.read()
bot = Bot(token=token)
dp = Dispatcher(bot=bot)


async def on_startup(_):
    print('Бот вышел в онлайн')

@dp.message_handler(commands=['start'])
async def process_start_command(msg: types.Message):
    await msg.answer("Привет!\nОтправь мне текст, а я сделаю из него QR-код.!")


@dp.message_handler(commands=['help'])
async def process_help_command(msg: types.Message):
    await msg.answer("Напиши мне что-нибудь, и я отправлю этот текст тебе в ответ!")


@dp.message_handler()
async def process_generator(msg: types.Message):
    await msg.answer("Секундочку, текст принят на обработку.")
    # file_name = msg.text
    qr_code = pq.create(msg.text)
    # qr_code.png(f'img/{file_name}.png', scale=6)
    qr_code.png('code.png', scale=8)
    with open('code.png', 'rb') as photo:
        await bot.send_photo(msg.chat.id, photo)
        await bot.send_message(msg.chat.id, 'Ваш QR-код готов, отправьте еще текст, чтобы сгенерировать новый')


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)