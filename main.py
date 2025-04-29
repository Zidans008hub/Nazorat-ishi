from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
import asyncio

TOKEN = "7801256857:AAHbteOqbjfvKSYJvEuDQSsLFidraNjAl4w"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Umumiy knopkalar soni va har sahifada nechta ko'rsatish
TOTAL_BUTTONS = 30
BUTTONS_PER_PAGE = 5

def get_keyboard(page: int = 0):
    builder = InlineKeyboardBuilder()
    start = page * BUTTONS_PER_PAGE + 1
    end = min(start + BUTTONS_PER_PAGE, TOTAL_BUTTONS + 1)
    for i in range(start, end):
        builder.button(text=str(i), callback_data=f"number:{i}")

    navigation_buttons = []
    if page > 0:
        navigation_buttons.append(InlineKeyboardButton(text="⬅️ Orqaga", callback_data=f"navigate:{page-1}"))
    if end <= TOTAL_BUTTONS:
        navigation_buttons.append(InlineKeyboardButton(text="➡️ Oldinga", callback_data=f"navigate:{page+1}"))

    builder.row(*navigation_buttons)
    return builder.as_markup()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Kerakli tugmani tanlang:", reply_markup=get_keyboard())

@dp.callback_query(lambda c: c.data.startswith('number:'))
async def number_callback(callback_query: CallbackQuery):
    number = callback_query.data.split(":")[1]
    await callback_query.answer(f"Siz {number}-tugmani bosdingiz!", show_alert=True)

@dp.callback_query(lambda c: c.data.startswith('navigate:'))
async def navigate_callback(callback_query: CallbackQuery):
    page = int(callback_query.data.split(":")[1])
    await callback_query.message.edit_reply_markup(reply_markup=get_keyboard(page))

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
