import asyncio
import logging
import redis
import datetime
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

logging.basicConfig(level=logging.INFO)

redis_client = redis.Redis(
    host='redis',
    port=6379,
    db=0,
    decode_responses=True
)
storage = RedisStorage(redis=redis_client)
bot = Bot(token="ВАШ_ТОКЕН")
dp = Dispatcher()

markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Help", callback_data="btnhelp")]
])

reset = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Reset", callback_data="btnReset")]
])



@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f"Йоу, {message.from_user.full_name}!", reply_markup=markup)

@dp.message(Command("help"))
async def cmd_help(message: Message):
    await message.reply("У меня есть такие крутые команды как:\n"
                        "/ping\n"
                        "/ping/my\n"
                        "/time")

@dp.message(Command("ping"))
async def cmd_ping(message: Message):
    user_id = str(message.from_user.id)
    redis_client.incr(f'ping_count:{user_id}')
    await message.reply("pong")

@dp.message(Command("ping_my"))
async def cmd_pingmy(message: Message):
    user_id = str(message.from_user.id)
    ping_count = redis_client.get(f'ping_count:{user_id}')
    if ping_count is not None:
        await message.answer(f"Вы использовали команду /ping {ping_count} раз.", reply_markup=reset)
    else:
        await message.answer("Вы использовали команду /ping 0 раз.")

@dp.message(Command("time"))
async def send_current_time(message: Message):
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%H:%M:%S")
    await message.answer(f"Текущее время: {formatted_time}")

@dp.callback_query(lambda c: c.data == 'btnReset')
async def process_btnreset(callback):
    user_id = str(callback.from_user.id)
    redis_client.delete(f'ping_count:{user_id}')
    await callback.message.edit_text("Ваша статистика сброшена!")

@dp.callback_query(lambda c: c.data == 'btnhelp')
async def process_btnhelp(callback_query):
    await callback_query.message.answer(f"У меня есть такие крутые команды как:\n"
                        "/ping\n"
                        "/ping_my\n"
                        "/time")
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())