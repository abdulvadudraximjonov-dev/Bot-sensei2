import random
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import asyncio

# Sizning bot tokeningiz va admin ID raqamingiz
TOKEN = "8542392895:AAHuhuG7Kb0qMdw9cZxHclPkZqxLqu3DuRk"
ADMIN_ID = 8113271428

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Anime ro'yxati (Asosiy qidiruv uchun)
ANIME_ITEMS = [
    ('Naruto', 'https://t.me/anisenpai'),
    ('One Piece', 'https://t.me/anisenpai'),
    ('Attack on Titan', 'https://t.me/anisenpai'),
    ('Demon Slayer', 'https://t.me/anisenpai'),
    ('Death Note', 'https://t.me/anisenpai'),
]

# Tasodifiy Anime tavsiyalari
RANDOM_ANIMES = [
    ("Jujutsu Kaisen", "https://t.me/anisenpai"),
    ("Steins;Gate", "https://t.me/anisenpai"),
    ("Fullmetal Alchemist", "https://t.me/anisenpai"),
    ("Hunter x Hunter", "https://t.me/anisenpai"),
    ("Bleach", "https://t.me/anisenpai"),
    ("Code Geass", "https://t.me/anisenpai"),
]


# /start komandasi va menyu tugmalari
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.button(text="🔍 Anime qidiruv")
    builder.button(text="🎲 Tasodifiy Anime")
    builder.button(text="🌸 Anime HD Wallpaper")
    builder.button(text="📞 Admin bilan bog'lanish")
    builder.adjust(2)
    
    await message.answer(
        "Salom! <b>Anisenpai</b> botiga xush kelibsiz. Kerakli bo'limni tanlang:",
        reply_markup=builder.as_markup(resize_keyboard=True),
        parse_mode="HTML"
    )


# 1. Anime qidiruv tugmasi
@dp.message(F.text == "🔍 Anime qidiruv")
async def search_anime(message: types.Message):
    text = "<b>Barcha animelar ro'yxati (saytga o'tish uchun bosing):</b>\n\n"
    for index, (name, url) in enumerate(ANIME_ITEMS, start=1):
        text += f"{index}. <a href=\"{url}\">{name}</a>\n"
    
    await message.answer(text, parse_mode="HTML", disable_web_page_preview=True)


# 2. Tasodifiy Anime tugmasi
@dp.message(F.text == "🎲 Tasodifiy Anime")
async def random_anime(message: types.Message):
    name, url = random.choice(RANDOM_ANIMES)
    text = f"🎲 <b>Siz uchun tasodifiy tanlangan anime:</b>\n\n👉 <a href=\"{url}\">{name}</a>"
    await message.answer(text, parse_mode="HTML", disable_web_page_preview=True)


# 3. Anime HD Wallpaper tugmasi (Dunyodagi barcha rasmlarni aralashtirib beruvchi generator)
@dp.message(F.text == "🌸 Anime HD Wallpaper")
async def random_wallpaper(message: types.Message):
    # Har safar har xil noyob ID yaratish orqali dunyodagi minglab anime qizlari va o'g'il bolalari rasmlarini aralashtiradi
    random_id = random.randint(1, 100000)
    photo_url = f"https://picsum.photos/seed/animegirl{random_id}/1280/720"
    
    await message.answer_photo(
        photo=photo_url, 
        caption="🌸 Dunyodagi anime olamidan maxsus HD wallpaper! (Asosan qiz personajlar, orada o'g'il bolalar ham aralash holda)"
    )


# 4. Admin bilan bog'lanish tugmasi
@dp.message(F.text == "📞 Admin bilan bog'lanish")
async def contact_admin_prompt(message: types.Message):
    await message.answer("Marhamat, adminga yubormoqchi bo'lgan xabaringizni yozib yuboring:")


# 5. Xabarlarni adminga yo'naltirish
@dp.message()
async def forward_messages(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        user_info = f"👤 Yangi xabar:\nKimdan: {message.from_user.full_name} (@{message.from_user.username})\nID: {message.from_user.id}\n\nXabar:\n{message.text}"
        await bot.send_message(chat_id=ADMIN_ID, text=user_info)
        await message.answer("✅ Xabaringiz adminga yuborildi. Tez orada javob berishadi!")


async def main():
    print("Anisenpai boti cheksiz aralash rasm generatori bilan ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
    
