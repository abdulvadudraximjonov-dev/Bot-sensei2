import random
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
import asyncio

TOKEN = "8542392895:AAHuhuG7Kb0qMdw9cZxHclPkZqxLqu3DuRk"
ADMIN_ID = 8113271428  # Sizning Admin ID raqamingiz

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Barcha foydalanuvchilar bazasi
users_db = {}

ANIME_ITEMS = [
    ('Naruto', 'https://animeaz.org/anime/naruto'),
    ('One Piece', 'https://animeaz.org/anime/one-piece'),
    ('Attack on Titan', 'https://animeaz.org/anime/attack-on-titan'),
    ('Demon Slayer', 'https://animeaz.org/anime/demon-slayer'),
    ('Death Note', 'https://animeaz.org/anime/death-note'),
]

RANDOM_ANIMES = [
    ("Naruto", "https://animeaz.org/anime/naruto"),
    ("Jujutsu Kaisen", "https://animeaz.org/anime/jujutsu-kaisen"),
    ("Attack on Titan", "https://animeaz.org/anime/attack-on-titan"),
    ("One Piece", "https://animeaz.org/anime/one-piece"),
    ("Demon Slayer", "https://animeaz.org/anime/demon-slayer"),
]

BRONZA_WALLPAPERS = [
    {"name": "Sakura (Naruto)", "photo": "https://images.unsplash.com/photo-1578632767115-351597cf2477"},
    {"name": "Nobara (Jujutsu Kaisen)", "photo": "https://images.unsplash.com/photo-1607604276583-eef5d076aa5f"},
    {"name": "Hinata (Naruto)", "photo": "https://images.unsplash.com/photo-1618336753974-aae8e04506aa"},
    {"name": "Asuna (Sword Art Online)", "photo": "https://images.unsplash.com/photo-1563089145-599997674d42"},
]

ANIME_WALLPAPERS = [
    "https://images.unsplash.com/photo-1578632767115-351597cf2477",
    "https://images.unsplash.com/photo-1607604276583-eef5d076aa5f",
    "https://images.unsplash.com/photo-1534447677768-be436bb09401",
    "https://images.unsplash.com/photo-1618336753974-aae8e04506aa",
]


@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    user_id = message.from_user.id
    args = message.text.split()
    user_name = message.from_user.full_name
    
    if user_id not in users_db:
        users_db[user_id] = {
            "points": 0,
            "refs": 0, 
            "harem": [], 
            "name": user_name,
            "username": message.from_user.username or "Yo'q"
        }
        
        if len(args) > 1:
            referrer_id = int(args[1])
            if referrer_id in users_db and referrer_id != user_id:
                users_db[referrer_id]["refs"] += 1
                users_db[referrer_id]["points"] += 2  # Har bir do'st uchun 2 ball
                
                try:
                    await bot.send_message(
                        referrer_id, 
                        f"🎉 Tabriklaymiz! <b>{user_name}</b> sizning havolangiz orqali qo'shildi.\n"
                        f"➕ Hisobingizga **2 ball** qo'shildi! Jami ballar: {users_db[referrer_id]['points']}"
                    )
                except:
                    pass

    builder = ReplyKeyboardBuilder()
    builder.button(text="🔍 Anime qidiruv")
    builder.button(text="🎲 Tasodifiy Anime")
    builder.button(text="🌸 Anime HD Wallpaper")
    builder.button(text="💖 Mening Haremim")
    builder.button(text="🎁 Waifu Tanlash (Bronza)")
    builder.button(text="👥 Referal (2 ball)")
    builder.button(text="🏆 Reyting va Ballar")
    
    # Faqat SIZGA (Admin uchun) maxsus boshqaruv tugmasi ko'rinadi
    if user_id == ADMIN_ID:
        builder.button(text="👑 Barcha Haremiklar (Admin)")
        
    builder.button(text="ℹ️ Bot haqida")
    builder.button(text="📞 Admin bilan bog'lanish")
    builder.adjust(2)
    
    await message.answer(
        "Salom! <b>Anisenpai</b> botiga xush kelibsiz. Kerakli bo'limni tanlang:",
        reply_markup=builder.as_markup(resize_keyboard=True),
        parse_mode="HTML"
    )


@dp.message(F.text == "🔍 Anime qidiruv")
async def search_anime(message: types.Message):
    builder = InlineKeyboardBuilder()
    for name, url in ANIME_ITEMS:
        builder.button(text=f"▶️ {name} ni tomosha qilish", url=url)
    builder.adjust(1)
    await message.answer("<b>Tomosha qilish uchun animeni tanlang:</b>", reply_markup=builder.as_markup(), parse_mode="HTML")


@dp.message(F.text == "🎲 Tasodifiy Anime")
async def random_anime(message: types.Message):
    name, url = random.choice(RANDOM_ANIMES)
    builder = InlineKeyboardBuilder()
    builder.button(text=f"🎬 {name} ni tomosha qilish", url=url)
    await message.answer(f"🎲 <b>Tasodifiy anime:</b> <b>{name}</b>", reply_markup=builder.as_markup(), parse_mode="HTML")


@dp.message(F.text == "🌸 Anime HD Wallpaper")
async def random_wallpaper(message: types.Message):
    photo_url = random.choice(ANIME_WALLPAPERS)
    await message.answer_photo(photo=photo_url, caption="🌸 Dunyodagi eng sara anime qiz personajlari HD wallpaper!")


@dp.message(F.text == "👥 Referal (2 ball)")
async def invite_friends(message: types.Message):
    user_id = message.from_user.id
    bot_info = await bot.get_me()
    ref_link = f"https://t.me/{bot_info.username}?start={user_id}"
    user_data = users_db.get(user_id, {"points": 0, "refs": 0})

    text = (
        f"👥 <b>Do'stlarni taklif qilish va Ball yig'ish:</b>\n\n"
        f"🔗 Sizning referal havolangiz:\n<code>{ref_link}</code>\n\n"
        f"📊 Taklif qilingan do'stlar: <b>{user_data['refs']} ta</b>\n"
        f"💎 Sizdagi jami ballar: <b>{user_data['points']} ball</b>\n"
        f"💡 <i>Har bir do'st uchun 2 ball beriladi!</i>"
    )
    await message.answer(text, parse_mode="HTML")


@dp.message(F.text == "🎁 Waifu Tanlash (Bronza)")
async def choose_waifu_menu(message: types.Message):
    user_id = message.from_user.id
    user_points = users_db.get(user_id, {}).get("points", 0)
    
    if user_points < 4:
        await message.answer(f"❌ Waifu tanlash uchun ballingiz yetarli emas! (Sizda: {user_points} ball, kerak: 4 ball)")
        return

    users_db[user_id]["points"] -= 4
    options = random.sample(BRONZA_WALLPAPERS, 3)
    
    builder = InlineKeyboardBuilder()
    for opt in options:
        builder.button(text=f"🌸 {opt['name']}", callback_data=f"pick_w:{opt['name']}")
    builder.adjust(1)
    
    await message.answer(
        "🎁 Quyidagi 3 ta waifudan **bittasini** tanlang:",
        reply_markup=builder.as_markup()
    )


@dp.callback_query(F.data.startswith("pick_w:"))
async def pick_waifu_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    waifu_name = callback.data.split(":", 1)[1]
    
    if user_id in users_db:
        if waifu_name not in users_db[user_id]["harem"]:
            users_db[user_id]["harem"].append(waifu_name)
    
    await callback.message.edit_text(f"✅ Tabriklaymiz! Siz tanladingiz:\n🌸 <b>{waifu_name}</b>")
    await callback.answer()


@dp.message(F.text == "💖 Mening Haremim")
async def my_harem(message: types.Message):
    user_id = message.from_user.id
    harem_list = users_db.get(user_id, {}).get("harem", [])
    
    if not harem_list:
        await message.answer("😔 Haremingiz hozircha bo'sh.")
    else:
        text = "💖 <b>Sizning Shaxsiy Haremingiz:</b>\n\n"
        for idx, w in enumerate(harem_list, 1):
            text += f"{idx}. 🌸 {w}\n"
        await message.answer(text, parse_mode="HTML")


@dp.message(F.text == "🏆 Reyting va Ballar")
async def leaderboard(message: types.Message):
    text = "🏆 <b>Foydalanuvchilar Reytingi:</b>\n\n"
    if not users_db:
        text += "Hali foydalanuvchilar yo'q."
    else:
        sorted_users = sorted(users_db.items(), key=lambda x: x[1]["points"], reverse=True)
        for idx, (uid, data) in enumerate(sorted_users, 1):
            harem_count = len(data["harem"])
            text += f"{idx}. 👤 {data['name']} — 💎 {data['points']} ball (Waifular: {harem_count} ta)\n"
    await message.answer(text, parse_mode="HTML")


# FAQAT SIZ UCHUN (ADMIN PANEL): Barcha foydalanuvchilarning haremi va ma'lumotlarini ko'rish
@dp.message(F.text == "👑 Barcha Haremiklar (Admin)")
async def admin_all_harems(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("❌ Bu bo'lim faqat admin uchun!")
        return
        
    text = f"👑 <b>Barcha foydalanuvchilarning Haremiklari ({len(users_db)} ta odam):</b>\n\n"
    
    if not users_db:
        text += "Hali botdan foydalanganlar yo'q."
    else:
        for uid, data in users_db.items():
            name = data["name"]
            points = data["points"]
            refs = data["refs"]
            harem_list = ", ".join(data["harem"]) if data["harem"] else "Hali waifusi yo'q"
            text += f"👤 <b>{name}</b> (ID: {uid})\n" \
                    f" ├── 💎 Ballar: {points} | Do'stlar: {refs} ta\n" \
                    f" └ 💖 Haremi: <i>{harem_list}</i>\n\n"
                    
    # Xabar uzun bo'lib ketganda bo'lib yuborish uchun qulaylik
    if len(text) > 4000:
        for x in range(0, len(text), 4000):
            await message.answer(text[x:x+4000], parse_mode="HTML")
    else:
        await message.answer(text, parse_mode="HTML")


@dp.message(F.text == "ℹ️ Bot haqida")
async def about_bot(message: types.Message):
    await message.answer("🤖 <b>Anisenpai Boti:</b> Anime tomosha qilish va shaxsiy harem tuzish o'yini!", parse_mode="HTML")


@dp.message(F.text == "📞 Admin bilan bog'lanish")
async def contact_admin_prompt(message: types.Message):
    await message.answer("Marhamat, adminga yubormoqchi bo'lgan xabaringizni yozing:")


@dp.message()
async def forward_messages(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        user_info = f"👤 Xabar:\nKimdan: {message.from_user.full_name} (@{message.from_user.username})\n\n{message.text}"
        await bot.send_message(chat_id=ADMIN_ID, text=user_info)
        await message.answer("✅ Xabaringiz adminga yuborildi.")


async def main():
    print("Anisenpai boti admin boshqaruvi bilan to'liq ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
