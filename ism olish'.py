from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio
import re

TOKEN = ""



bot = Bot(token=TOKEN)
dp = Dispatcher()

user_states = {}


ASKING_NAME = "asking_name"
ASKING_PHONE = "asking_phone"

@dp.message(Command("start"))
async def start(message: types.Message):
    user_states[message.from_user.id] = ASKING_NAME
    await message.answer("Ismingizni kiriting:")

@dp.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    state = user_states.get(user_id)

    if not state:
        await message.answer("Iltimos, /start buyrug'ini bosing.")
        return

    text = message.text.strip()

    if text.lower() == "help":
        if state == ASKING_NAME:
            await message.answer("Ismni kiritishda o'z ismingizni yozing. Masalan: Ali, Zayniddin.")
        elif state == ASKING_PHONE:
            await message.answer("Telefon raqamni +998 bilan yoki 99 999 99 99 shaklida kiriting.\nMasalan: +998901234567 yoki 90 123 45 67.")
        return

    if state == ASKING_NAME:

        user_states[user_id] = ASKING_PHONE
        await message.answer(f"Rahmat, {text}! Endi telefon raqamingizni kiriting:")

    elif state == ASKING_PHONE:
        if validate_phone(text):
            user_states.pop(user_id, None)
            await message.answer(f"Raqamingiz: {text} qabul qilindi. Rahmat!")
        else:
            await message.answer("❌ Xato! Telefon raqamni to‘g‘ri formatda kiriting.\nNamuna: +998901234567 yoki 90 123 45 67\nYordam uchun: help")

def validate_phone(phone: str) -> bool:
    """
    Telefon raqamni tekshiradi.
    - +998 bilan boshlansa 13 ta belgidan iborat bo'lishi kerak (+998*********).
    - Agar faqat raqamlar bo'lsa va oralarida bo'sh joy bo'lsa, 9 yoki 12 ta raqam bo'lishi mumkin.
    """
    phone = phone.replace(" ", "")  # bo'sh joylarni olib tashlaymiz
    if phone.startswith("+998") and len(phone) == 13 and phone[1:].isdigit():
        return True
    if len(phone) == 9 and phone.isdigit():
        return True
    return False

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
