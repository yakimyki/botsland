import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
import asyncio

TOKEN = token=os.environ.get('TOKEN')
CHANNEL_USERNAME = "@worldstockAI"
GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/1J6GyaS_gSqG0ActRdwRUgN4iqW5y9ZgVqr0NvJzYCeQ/edit?gid=354812718#gid=354812718"

logging.basicConfig(level=logging.INFO)


bot = Bot(TOKEN)
dp = Dispatcher(bot)

# Создание клавиатуры с кнопками
def get_subscription_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    subscribe_button = InlineKeyboardButton(
        text="📢 Подписаться", url=f"https://t.me/{CHANNEL_USERNAME[1:]}"
    )
    check_button = InlineKeyboardButton(text="🔄 Проверить подписку", callback_data="check_sub")
    keyboard.add(subscribe_button, check_button)
    return keyboard

# Функция проверки подписки
async def check_subscription(user_id):
    chat_member = await bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
    return chat_member.status in ["member", "administrator", "creator"]

# Обработчик команды /start
@dp.message(commands=["start"])
async def start_command(message: types.Message):
    user_id = message.from_user.id
    if await check_subscription(user_id):
        keyboard = InlineKeyboardMarkup(row_width=1)
        sheet_button = InlineKeyboardButton("📄 Открыть Google Таблицу", url=GOOGLE_SHEET_URL)
        keyboard.add(sheet_button)
        await message.answer("✅ Вы подписаны! Вот ваша ссылка на Google Таблицу", reply_markup=keyboard)
    else:
        await message.answer(
            "⚠️ Пожалуйста, подпишитесь на мой канал, чтобы получить доступ к Google Таблице!",
            reply_markup=get_subscription_keyboard()
        )

# Обработчик кнопки "Проверить подписку"
@dp.callback_query_handler(lambda call: call.data == "check_sub")
async def check_subscription_callback(call: types.CallbackQuery):
    user_id = call.from_user.id
    if await check_subscription(user_id):
        keyboard = InlineKeyboardMarkup(row_width=1)
        sheet_button = InlineKeyboardButton("📄 Открыть Google Таблицу", url=GOOGLE_SHEET_URL)
        keyboard.add(sheet_button)
        await call.message.edit_text("✅ Вы подписаны! Вот ваша ссылка на Google Таблицу", reply_markup=keyboard)
    else:
        await call.answer("⚠️ Вы пока не подписаны на канал!", show_alert=True)

# Запуск бота
async def main():
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())
