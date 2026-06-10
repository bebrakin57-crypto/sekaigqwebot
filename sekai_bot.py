from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.exceptions import TelegramNetworkError
from datetime import datetime, timedelta
import asyncio
import json
import os
import random

TOKEN = os.getenv("TOKEN", "")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# ========== ДАННЫЕ ==========
ADMINS = [8692814125, 5948595089]
users = {}
DATA_FILE = "sekai_users.json"

PRICE_PER_PULL = 300
PRICE_10_PULLS = 3000

# ========== БОНУСЫ ==========
DAILY_BONUS = 3000
HOURLY_BONUS = 300
HOURLY_BONUS_SUB = 450
NEWS_CHANNEL = "@PJSKgachanews"

# ========== АДМИН ЛОГИ ==========
admin_logs = []
new_users_log = []
ADMIN_LOG_FILE = "admin_logs.json"
NEW_USERS_FILE = "new_users.json"

# ========== НАСТРОЙКИ ПОДПИСКИ ==========
CHECK_SUBSCRIPTION = False

# Хранилища
last_hourly_bonus = {}
promocodes = {}
used_promocodes = {}
pull_context = {}

# ========== ГИФКИ (file_id) ==========
GIF_4_STAR = "CgACAgIAAxkBAAIDWWooa7ScaSH2ibrZ4QGzBU_FhE9gAALUmAACHvtBSbNKNbm2bYmAOwQ"
GIF_3_STAR = "CgACAgIAAxkBAAIDXWooa-sG27Ij3A5BvpMOjEI3LNPMAALZmAACHvtBSaS50MPd5M6mOwQ"
GIF_2_STAR = "CgACAgIAAxkBAAIDX2ooa_yDyKGgNeZb7TC3SPSzhNebAALamAACHvtBST8t-aiS1x37OwQ"

# ========== ПЕРСОНАЖИ ==========
characters_4star = [
    {"name": "🎤 Хацунэ Мику", "rarity": 4, "stars": "★★★★"},
    {"name": "🎸 Кагаминэ Рин", "rarity": 4, "stars": "★★★★"},
    {"name": "🎸 Кагаминэ Лэн", "rarity": 4, "stars": "★★★★"},
    {"name": "🎵 Мегуринэ Лука", "rarity": 4, "stars": "★★★★"},
    {"name": "🍷 Мейко", "rarity": 4, "stars": "★★★★"},
    {"name": "❄️ Кайто", "rarity": 4, "stars": "★★★★"},
    {"name": "🎸 Хосино Ичика", "rarity": 4, "stars": "★★★★"},
    {"name": "🎹 Тэмма Саки", "rarity": 4, "stars": "★★★★"},
    {"name": "🥧 Мотидзуки Хонами", "rarity": 4, "stars": "★★★★"},
    {"name": "🎸 Хинамори Сихо", "rarity": 4, "stars": "★★★★"},
    {"name": "☁️ Ханасато Минори", "rarity": 4, "stars": "★★★★"},
    {"name": "⭐ Киритани Харука", "rarity": 4, "stars": "★★★★"},
    {"name": "🌸 Момои Айри", "rarity": 4, "stars": "★★★★"},
    {"name": "💫 Хинамори Сизуку", "rarity": 4, "stars": "★★★★"},
    {"name": "🐹 Адзусава Кохане", "rarity": 4, "stars": "★★★★"},
    {"name": "🎤 Сираиси Ан", "rarity": 4, "stars": "★★★★"},
    {"name": "🎧 Синонага Акито", "rarity": 4, "stars": "★★★★"},
    {"name": "🎹 Аояги Тоя", "rarity": 4, "stars": "★★★★"},
    {"name": "⭐ Тэнма Цукаса", "rarity": 4, "stars": "★★★★"},
    {"name": "🎭 Отори Эму", "rarity": 4, "stars": "★★★★"},
    {"name": "🎮 Кусуноки Нэнэ", "rarity": 4, "stars": "★★★★"},
    {"name": "🎭 Камисиро Руи", "rarity": 4, "stars": "★★★★"},
    {"name": "🎧 Ёйсаки Канадэ", "rarity": 4, "stars": "★★★★"},
    {"name": "🌙 Асахина Мафую", "rarity": 4, "stars": "★★★★"},
    {"name": "🎨 Синомика Эна", "rarity": 4, "stars": "★★★★"},
    {"name": "🎭 Акияма Мидзуки", "rarity": 4, "stars": "★★★★"},
]

characters_3star = [
# VIRTUAL SINGER (6)
{"name": "🎤 Хатсунэ Мику", "rarity": 3, "stars": "★★★", "unit": "VS"},
{"name": "🎸 Кагамине Рин", "rarity": 3, "stars": "★★★", "unit": "VS"},
{"name": "🎸 Кагамине Лен", "rarity": 3, "stars": "★★★", "unit": "VS"},
{"name": "🎵 Мегурине Лука", "rarity": 3, "stars": "★★★", "unit": "VS"},
{"name": "🍷 Мейко", "rarity": 3, "stars": "★★★", "unit": "VS"},
{"name": "❄️ Кайто", "rarity": 3, "stars": "★★★", "unit": "VS"},

# Leo/need (4)
{"name": "🎸 Хошино Ичика", "rarity": 3, "stars": "★★★", "unit": "Leo/need"},
{"name": "🎹 Тенма Саки", "rarity": 3, "stars": "★★★", "unit": "Leo/need"},
{"name": "🥧 Мочизуки Хонами", "rarity": 3, "stars": "★★★", "unit": "Leo/need"},
{"name": "🎸 Хиномори Шихо", "rarity": 3, "stars": "★★★", "unit": "Leo/need"},

# MORE MORE JUMP! (4)
{"name": "☁️ Ханасато Минори", "rarity": 3, "stars": "★★★", "unit": "MMJ"},
{"name": "⭐️ Киритани Харука", "rarity": 3, "stars": "★★★", "unit": "MMJ"},
{"name": "🌸 Момои Аири", "rarity": 3, "stars": "★★★", "unit": "MMJ"},
{"name": "💫 Хиномори Шизуку", "rarity": 3, "stars": "★★★", "unit": "MMJ"},

# Vivid BAD SQUAD (4)
{"name": "🐹 Азусава Кохане", "rarity": 3, "stars": "★★★", "unit": "VBS"},
{"name": "🎤 Шираиши Ан", "rarity": 3, "stars": "★★★", "unit": "VBS"},
{"name": "🎧 Шинономе Акито", "rarity": 3, "stars": "★★★", "unit": "VBS"},
{"name": "🎹 Аояги Тойя", "rarity": 3, "stars": "★★★", "unit": "VBS"},

# Wonderlands×Showtime (4)
{"name": "⭐️ Тенма Цукаса", "rarity": 3, "stars": "★★★", "unit": "W×S"},
{"name": "🎭 Отори Эму", "rarity": 3, "stars": "★★★", "unit": "W×S"},
{"name": "🎮 Кусуноги Нене", "rarity": 3, "stars": "★★★", "unit": "W×S"},
{"name": "🎭 Камиширо Руи", "rarity": 3, "stars": "★★★", "unit": "W×S"},

# 25-ji, Nightcord de. (4)
{"name": "🎧 Йоисаки Канаде", "rarity": 3, "stars": "★★★", "unit": "25-ji"},
{"name": "🌙 Асахина Мафую", "rarity": 3, "stars": "★★★", "unit": "25-ji"},
{"name": "🎨 Шинономе Эна", "rarity": 3, "stars": "★★★", "unit": "25-ji"},
{"name": "🎭 Акияма Мизуки", "rarity": 3, "stars": "★★★", "unit": "25-ji"},
]

characters_2star = [
# VIRTUAL SINGER (6)
{"name": "🎤 Хатсуне Мику", "rarity": 2, "stars": "★★", "unit": "VS"},
{"name": "🎸 Кагамине Рин", "rarity": 2, "stars": "★★", "unit": "VS"},
{"name": "🎸 Кагамине Лен", "rarity": 2, "stars": "★★", "unit": "VS"},
{"name": "🎵 Мегурине Лука", "rarity": 2, "stars": "★★", "unit": "VS"},
{"name": "🍷 Мейко", "rarity": 2, "stars": "★★", "unit": "VS"},
{"name": "❄️ Кайто", "rarity": 2, "stars": "★★", "unit": "VS"},

# Leo/need (4)
{"name": "🎸 Хошино Ичика", "rarity": 2, "stars": "★★", "unit": "Leo/need"},
{"name": "🎹 Тенма Саки", "rarity": 2, "stars": "★★", "unit": "Leo/need"},
{"name": "🥧 Мочизуки Хонами", "rarity": 2, "stars": "★★", "unit": "Leo/need"},
{"name": "🎸 Хиномори Шихо", "rarity": 2, "stars": "★★", "unit": "Leo/need"},

# MORE MORE JUMP! (4)
{"name": "☁️ Ханасато Минори", "rarity": 2, "stars": "★★", "unit": "MMJ"},
{"name": "⭐️ Киритани Харука", "rarity": 2, "stars": "★★", "unit": "MMJ"},
{"name": "🌸 Момои Аири", "rarity": 2, "stars": "★★", "unit": "MMJ"},
{"name": "💫 Хиномори Шизуку", "rarity": 2, "stars": "★★", "unit": "MMJ"},

 # Vivid BAD SQUAD (4)
{"name": "🐹 Азусава Кохане", "rarity": 2, "stars": "★★", "unit": "VBS"},
{"name": "🎤 Шираиши Ан", "rarity": 2, "stars": "★★", "unit": "VBS"},
{"name": "🎧 Шинономе Акито", "rarity": 2, "stars": "★★", "unit": "VBS"},
{"name": "🎹 Аояги Тойя", "rarity": 2, "stars": "★★", "unit": "VBS"},

 # Wonderlands×Showtime (4)
{"name": "⭐️ Тенма Цукаса", "rarity": 2, "stars": "★★", "unit": "W×S"},
{"name": "🎭 Отори Эму", "rarity": 2, "stars": "★★", "unit": "W×S"},
{"name": "🎮 Кусуноги Нене", "rarity": 2, "stars": "★★", "unit": "W×S"},
{"name": "🎭 Камиширо Руи", "rarity": 2, "stars": "★★", "unit": "W×S"},

# 25-ji, Nightcord de. (4)
{"name": "🎧 Йоисаки Канаде", "rarity": 2, "stars": "★★", "unit": "25-ji"},
{"name": "🌙 Асахина Мафую", "rarity": 2, "stars": "★★", "unit": "25-ji"},
{"name": "🎨 Шинономе Эна", "rarity": 2, "stars": "★★", "unit": "25-ji"},
{"name": "🎭 Акияма Мизуки", "rarity": 2, "stars": "★★", "unit": "25-ji"},
]

BASE_RATE_4_STAR = 3.0
BASE_RATE_3_STAR = 8.5
SOFT_PITY_START = 75
HARD_PITY = 100


def load_data():
    global users, promocodes, used_promocodes
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            users = data.get("users", {})
            promocodes = data.get("promocodes", {})
            used_promocodes = data.get("used_promocodes", {})
    else:
        users = {}
        promocodes = {}
        used_promocodes = {}
    save_data()
    load_admin_logs()
    load_new_users_log()


def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "users": users,
            "promocodes": promocodes,
            "used_promocodes": used_promocodes
        }, f, ensure_ascii=False, indent=2)


def save_admin_logs():
    with open(ADMIN_LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(admin_logs, f, ensure_ascii=False, indent=2)


def load_admin_logs():
    global admin_logs
    if os.path.exists(ADMIN_LOG_FILE):
        with open(ADMIN_LOG_FILE, "r", encoding="utf-8") as f:
            admin_logs = json.load(f)


def save_new_users_log():
    with open(NEW_USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(new_users_log, f, ensure_ascii=False, indent=2)


def load_new_users_log():
    global new_users_log
    if os.path.exists(NEW_USERS_FILE):
        with open(NEW_USERS_FILE, "r", encoding="utf-8") as f:
            new_users_log = json.load(f)


def pull_gacha_with_pity(user_id):
    pity_4 = users[user_id].get("pity_4", 0)

    if pity_4 >= HARD_PITY - 1:
        item = random.choice(characters_4star).copy()
        item["rarity"] = 4
        users[user_id]["pity_4"] = 0
        return item

    if pity_4 >= SOFT_PITY_START:
        bonus = (pity_4 - SOFT_PITY_START + 1) * 5
        current_rate = BASE_RATE_4_STAR + min(bonus, 100 - BASE_RATE_4_STAR)
    else:
        current_rate = BASE_RATE_4_STAR

    roll = random.random() * 100

    if roll < current_rate:
        item = random.choice(characters_4star).copy()
        item["rarity"] = 4
        users[user_id]["pity_4"] = 0
    elif roll < (current_rate + BASE_RATE_3_STAR):
        item = random.choice(characters_3star).copy()
        item["rarity"] = 3
        users[user_id]["pity_4"] = pity_4 + 1
    else:
        # ТЕПЕРЬ ТУТ ВЫПАДАЮТ 2★ ПЕРСОНАЖИ, А НЕ ПРЕДМЕТЫ!
        item = random.choice(characters_2star).copy()
        item["rarity"] = 2
        users[user_id]["pity_4"] = pity_4 + 1

    return item


def pull_ten_with_guarantee(user_id):
    results = []
    count_4 = 0
    count_3 = 0

    for i in range(9):
        result = pull_gacha_with_pity(user_id)
        results.append(result)
        if result["rarity"] == 4:
            count_4 += 1
        elif result["rarity"] == 3:
            count_3 += 1

    had_3star_or_higher = (count_3 > 0 or count_4 > 0)

    if not had_3star_or_higher:
        guaranteed_3star = random.choice(characters_3star).copy()
        guaranteed_3star["rarity"] = 3
        results.append(guaranteed_3star)
        count_3 += 1
        users[user_id]["pity_4"] = users[user_id].get("pity_4", 0) + 1
    else:
        result = pull_gacha_with_pity(user_id)
        results.append(result)
        if result["rarity"] == 4:
            count_4 += 1
        elif result["rarity"] == 3:
            count_3 += 1

    return results, count_4, count_3


# ========== КОМАНДЫ ==========
@dp.message(Command("start"))
async def start(message: types.Message):
    user_id = str(message.from_user.id)
    is_new = user_id not in users

    subscribed = False
    if CHECK_SUBSCRIPTION:
        try:
            chat_member = await bot.get_chat_member(NEWS_CHANNEL, int(user_id))
            if chat_member.status in ["member", "creator", "administrator"]:
                subscribed = True
        except:
            pass

    if is_new:
        users[user_id] = {
            "primogems": 3000,
            "inventory": [],
            "last_daily": None,
            "last_hourly": None,
            "total_pulls": 0,
            "pity_4": 0,
            "name": message.from_user.first_name
        }
        save_data()

        new_user_entry = {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "user_id": user_id,
            "user_name": message.from_user.username or "Нет юзернейма",
            "first_name": message.from_user.first_name
        }
        new_users_log.append(new_user_entry)
        save_new_users_log()

        for admin in ADMINS:
            try:
                await bot.send_message(admin, f"🆕 НОВЫЙ ПОЛЬЗОВАТЕЛЬ!\n\n👤 {message.from_user.first_name}\n🆔 {user_id}")
            except:
                pass

    daily_bonus = int(DAILY_BONUS * 1.5) if subscribed else DAILY_BONUS
    hourly_bonus = int(HOURLY_BONUS_SUB) if subscribed else HOURLY_BONUS

    await message.answer(
        f"✨ Добро пожаловать в Project SEKAI Гача! ✨\n\n"
        f"💎 Твои кристаллы: {users[user_id]['primogems']}\n\n"
        f"🎮 /pull - 1 крутка\n"
        f"🎮 /pull10 - 10 круток\n"
        f"📦 /inventory - коллекция\n"
        f"📊 /stats - статистика\n"
        f"🎯 /rates - шансы\n\n"
        f"🎁 /daily - {daily_bonus} кристаллов\n"
        f"⏰ Каждый час - {hourly_bonus} кристаллов\n"
        f"🎫 /promo КОД - промокод\n"
        f"📋 /my_promos - мои промокоды\n\n"
        f"📢 Новостной канал: {NEWS_CHANNEL}\n"
        f"🎁 Бонус за подписку: +50%\n"
        f"✅ /check_sub - проверить подписку"
    )


@dp.message(Command("pull"))
async def pull(message: types.Message):
    user_id = str(message.from_user.id)

    if user_id not in users:
        await message.answer("❌ Напиши /start")
        return

    if users[user_id]["primogems"] < PRICE_PER_PULL:
        await message.answer(f"❌ Не хватает! Нужно {PRICE_PER_PULL}")
        return

    if "pity_4" not in users[user_id]:
        users[user_id]["pity_4"] = 0

    # Сразу делаем крутку, чтобы узнать результат
    result = pull_gacha_with_pity(user_id)

    # Отправляем ГИФКУ в зависимости от редкости (сразу с первой секунды)
    if result["rarity"] == 4:
        gif_msg = await message.answer_video(video=GIF_4_STAR, supports_streaming=True)
    elif result["rarity"] == 3:
        gif_msg = await message.answer_video(video=GIF_3_STAR, supports_streaming=True)
    else:
        gif_msg = await message.answer_video(video=GIF_2_STAR, supports_streaming=True)

    # Кнопка пропуска
    skip_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⏩ ПОКАЗАТЬ РЕЗУЛЬТАТ", callback_data=f"show_{user_id}")]
    ])

    try:
        await gif_msg.edit_caption(caption="🎴 Крутка... (нажмите кнопку)", reply_markup=skip_kb)
    except:
        pass

    # Сохраняем результат в контекст (но не списываем кристаллы еще!)
    pull_context[user_id] = {"is_ten": False, "result": result, "message_id": gif_msg.message_id,
                             "chat_id": gif_msg.chat.id}


@dp.message(Command("pull10"))
async def pull_ten(message: types.Message):
    user_id = str(message.from_user.id)

    if user_id not in users:
        await message.answer("❌ Напиши /start")
        return

    if users[user_id]["primogems"] < PRICE_10_PULLS:
        await message.answer(f"❌ Не хватает! Нужно {PRICE_10_PULLS}")
        return

    if "pity_4" not in users[user_id]:
        users[user_id]["pity_4"] = 0

    # Сразу делаем 10 круток, чтобы узнать результат
    results, count_4, count_3 = pull_ten_with_guarantee(user_id)

    # Отправляем ГИФКУ в зависимости от редкости
    if count_4 > 0:
        gif_msg = await message.answer_video(video=GIF_4_STAR, supports_streaming=True)
    elif count_3 > 0:
        gif_msg = await message.answer_video(video=GIF_3_STAR, supports_streaming=True)
    else:
        gif_msg = await message.answer_video(video=GIF_2_STAR, supports_streaming=True)

    # Кнопка пропуска
    skip_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⏩ ПОКАЗАТЬ РЕЗУЛЬТАТ", callback_data=f"show_{user_id}")]
    ])

    try:
        await gif_msg.edit_caption(caption="🎴 10 круток... (нажмите кнопку)", reply_markup=skip_kb)
    except:
        pass

    # Сохраняем результат в контекст
    pull_context[user_id] = {"is_ten": True, "result": results, "message_id": gif_msg.message_id,
                             "chat_id": gif_msg.chat.id}


@dp.callback_query(lambda c: c.data.startswith("show_"))
async def show_result(callback: types.CallbackQuery):
    user_id = callback.data.split("_")[1]

    # Удаляем сообщение с гифкой
    try:
        await callback.message.delete()
    except:
        pass

    ctx = pull_context.get(user_id, {})
    is_ten = ctx.get("is_ten", False)
    result = ctx.get("result")

    if not result:
        await callback.message.answer("❌ Ошибка: результат не найден")
        await callback.answer()
        return

    if is_ten:
        # 10 КРУТОК
        results = result
        count_4 = sum(1 for r in results if r["rarity"] == 4)
        count_3 = sum(1 for r in results if r["rarity"] == 3)

        # Списываем кристаллы
        users[user_id]["primogems"] -= PRICE_10_PULLS
        users[user_id]["total_pulls"] = users[user_id].get("total_pulls", 0) + 10
        for r in results:
            users[user_id]["inventory"].append(r)
        save_data()

        text_result = f"✨✨✨ РЕЗУЛЬТАТ 10 КРУТОК ✨✨✨\n\n"
        text_result += f"🌈 4★: {count_4} шт.\n"
        text_result += f"💛 3★: {count_3} шт.\n\n"
        for r in results:
            star_display = {4: "🌈", 3: "💛", 2: "💙"}[r["rarity"]]
            text_result += f"{star_display} {r['stars']} {r['name']}\n"
        text_result += f"\n💎 Осталось: {users[user_id]['primogems']}"
        text_result += f"\n📊 До гаранта 4★: {HARD_PITY - users[user_id]['pity_4']} круток"
        await callback.message.answer(text_result[:4000])
    else:
        # 1 КРУТКА
        stars = result["stars"]
        color = {4: "🌈", 3: "💛", 2: "💙"}[result["rarity"]]
        pity_msg = f"\n📊 До гаранта 4★: {HARD_PITY - users[user_id]['pity_4']} круток" if result[
                                                                                              "rarity"] != 4 else "\n📊 Pity сброшен!"

        # Списываем кристаллы
        users[user_id]["primogems"] -= PRICE_PER_PULL
        users[user_id]["total_pulls"] = users[user_id].get("total_pulls", 0) + 1
        users[user_id]["inventory"].append(result)
        save_data()

        await callback.message.answer(
            f"{color} ВЫПАЛО: {result['name']}\n{stars}\n\n"
            f"💎 Осталось: {users[user_id]['primogems']}{pity_msg}"
        )

    if user_id in pull_context:
        del pull_context[user_id]
    await callback.answer()


@dp.message(Command("daily"))
async def daily_reward(message: types.Message):
    user_id = str(message.from_user.id)
    if user_id not in users:
        await message.answer("❌ Напиши /start")
        return

    today = datetime.now().date()
    last = users[user_id].get("last_daily")
    if last and datetime.strptime(last, "%Y-%m-%d").date() == today:
        await message.answer("🎁 Ты уже получал бонус сегодня! Приходи завтра.")
        return

    bonus_amount = DAILY_BONUS
    subscribed = False
    try:
        chat_member = await bot.get_chat_member(NEWS_CHANNEL, int(user_id))
        if chat_member.status in ["member", "creator", "administrator"]:
            subscribed = True
            bonus_amount = int(DAILY_BONUS * 1.5)
    except:
        pass

    users[user_id]["primogems"] += bonus_amount
    users[user_id]["last_daily"] = today.isoformat()
    save_data()

    pulls = bonus_amount // 300
    sub_text = " (с бонусом за подписку)" if subscribed else ""

    await message.answer(
        f"🎁 Ежедневный бонус!{sub_text}\n💎 +{bonus_amount} кристаллов\n🎰 {pulls} круток\n\n💎 Всего: {users[user_id]['primogems']} ({users[user_id]['primogems'] // 300} круток)")


@dp.message(Command("inventory"))
async def inventory(message: types.Message):
    user_id = str(message.from_user.id)
    if user_id not in users or not users[user_id]["inventory"]:
        await message.answer("📦 Пусто! /pull")
        return

    count = {}
    for item in users[user_id]["inventory"]:
        name = item["name"]
        count[name] = count.get(name, 0) + 1

    text = "📦 КОЛЛЕКЦИЯ 📦\n\n"
    for name, c in count.items():
        for char in characters_4star:
            if char["name"] == name:
                text += f"🌈 {char['stars']} {name} x{c}\n"
    for name, c in count.items():
        for char in characters_3star:
            if char["name"] == name:
                text += f"💛 {char['stars']} {name} x{c}\n"
    # Вместо items_2star используем characters_2star
    for name, c in count.items():
        for char in characters_2star:
            if char["name"] == name:
                text += f"💙 {char['stars']} {name} x{c}\n"

    await message.answer(text[:4000])


@dp.message(Command("stats"))
async def stats(message: types.Message):
    user_id = str(message.from_user.id)
    data = users[user_id]
    count_4 = sum(1 for i in data["inventory"] if i.get("rarity") == 4)
    pity_4 = data.get("pity_4", 0)

    await message.answer(
        f"📊 СТАТИСТИКА 📊\n\n"
        f"💎 Кристаллов: {data['primogems']}\n"
        f"🎯 Круток: {data.get('total_pulls', 0)}\n"
        f"🌈 4★: {count_4}\n"
        f"📦 Предметов: {len(data['inventory'])}\n\n"
        f"📊 Счетчик pity:\n🎯 До гаранта 4★: {HARD_PITY - pity_4} круток"
    )


@dp.message(Command("rates"))
async def show_rates(message: types.Message):
    await message.answer(
        "🎲 ШАНСЫ ВЫПАДЕНИЯ 🎲\n\n"
        "🌈 4★ карта: 3% (базовый)\n"
        "💛 3★ карта: 8.5%\n"
        "💙 2★ предмет: 88.5%\n\n"
        "🎯 СИСТЕМА ГАРАНТОВ:\n"
        f"• Гарант 4★: на {HARD_PITY} крутке\n"
        f"• Мягкий pity: с {SOFT_PITY_START} крутки\n"
        "• Гарант 3★+: в каждой 10 крутке\n\n"
        f"💰 1 крутка = {PRICE_PER_PULL} кристаллов"
    )


@dp.message(Command("promo"))
async def use_promo(message: types.Message):
    user_id = str(message.from_user.id)
    if user_id not in users:
        await message.answer("❌ Напиши /start")
        return

    parts = message.text.split()
    if len(parts) < 2:
        await message.answer("❌ /promo КОД\n\nПример: /promo SEKAIGEMS")
        return

    code = parts[1].upper()
    if code not in promocodes:
        await message.answer(f"❌ Промокод {code} не найден!")
        return

    promo = promocodes[code]

    if promo["expires"]:
        expires = datetime.strptime(promo["expires"], "%Y-%m-%d %H:%M:%S")
        if datetime.now() > expires:
            await message.answer(f"❌ Промокод {code} истек!")
            return

    if promo["max_uses"] > 0 and promo["uses"] >= promo["max_uses"]:
        await message.answer(f"❌ Промокод {code} уже использован максимальное количество раз!")
        return

    if user_id not in used_promocodes:
        used_promocodes[user_id] = []

    if code in used_promocodes[user_id]:
        await message.answer(f"❌ Ты уже активировал промокод {code}!")
        return

    reward = promo["reward"]
    users[user_id]["primogems"] += reward
    promo["uses"] += 1
    used_promocodes[user_id].append(code)
    save_data()

    await message.answer(
        f"✅ Промокод {code} активирован!\n\n💎 +{reward} кристаллов\n🎰 +{reward // 300} круток\n\n💎 Всего: {users[user_id]['primogems']} ({users[user_id]['primogems'] // 300} круток)")


@dp.message(Command("my_promos"))
async def my_promos(message: types.Message):
    user_id = str(message.from_user.id)
    if user_id not in users:
        await message.answer("❌ Напиши /start")
        return

    if user_id not in used_promocodes or not used_promocodes[user_id]:
        await message.answer("📭 Ты еще не активировал ни одного промокода")
        return

    text = "🎫 ТВОИ АКТИВИРОВАННЫЕ ПРОМОКОДЫ 🎫\n\n"
    for code in used_promocodes[user_id]:
        text += f"✅ {code}\n"

    await message.answer(text)


@dp.message(Command("check_sub"))
async def check_subscription(message: types.Message):
    user_id = str(message.from_user.id)
    if user_id not in users:
        await message.answer("❌ Напиши /start")
        return

    try:
        chat_member = await bot.get_chat_member(NEWS_CHANNEL, int(user_id))
        if chat_member.status in ["member", "creator", "administrator"]:
            await message.answer(f"✅ Ты подписан на {NEWS_CHANNEL}\n🎁 Бонус: +50% к кристаллам!")
        else:
            await message.answer(f"❌ Ты не подписан на {NEWS_CHANNEL}\n📢 Подпишись, чтобы получать +50% к бонусам!")
    except:
        await message.answer(f"⚠️ Не удалось проверить подписку. Убедись, что канал {NEWS_CHANNEL} существует.")


@dp.message(Command("support"))
async def support_command(message: types.Message):
    SUPPORT_BOT_USERNAME = "PJSK_SupportBot"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🆘 Написать в поддержку", url=f"https://t.me/{SUPPORT_BOT_USERNAME}")]
    ])
    await message.answer(
        "🆘 **Поддержка Project SEKAI Гача**\n\nЕсли у вас возникли проблемы, напишите в нашу службу поддержки.\n\n📌 **Нажмите на кнопку ниже**",
        reply_markup=keyboard
    )


# ========== АДМИН-КОМАНДЫ ==========
@dp.message(Command("allusers"))
async def all_users(message: types.Message):
    if message.from_user.id not in ADMINS:
        await message.answer("❌ Только для админа!")
        return

    if not users:
        await message.answer("📭 Нет пользователей")
        return

    text = "👥 ПОЛЬЗОВАТЕЛИ:\n\n"
    for uid, data in users.items():
        name = data.get("name", "Без имени")
        text += f"🆔 {uid} | 👤 {name} | 💎 {data['primogems']} | 🎯 {data.get('total_pulls', 0)}\n"

    await message.answer(text[:4000])


@dp.message(Command("addgems"))
async def add_gems(message: types.Message):
    if message.from_user.id not in ADMINS:
        await message.answer("❌ Только для админа!")
        return

    parts = message.text.split()
    if len(parts) < 3:
        await message.answer("❌ /addgems user_id количество")
        return

    target = parts[1]
    try:
        amount = int(parts[2])
    except:
        await message.answer("❌ Число!")
        return

    if target not in users:
        await message.answer(f"❌ {target} не найден")
        return

    users[target]["primogems"] += amount
    save_data()
    await message.answer(f"✅ +{amount} кристаллов {target}")


@dp.message(Command("setgems"))
async def set_gems(message: types.Message):
    if message.from_user.id not in ADMINS:
        await message.answer("❌ Только для админа!")
        return

    parts = message.text.split()
    if len(parts) < 3:
        await message.answer("❌ /setgems user_id количество\n\nПример: /setgems 123456789 5000")
        return

    target = parts[1]
    try:
        amount = int(parts[2])
    except:
        await message.answer("❌ Количество должно быть числом!")
        return

    if target not in users:
        await message.answer(f"❌ Пользователь {target} не найден")
        return

    old_gems = users[target]["primogems"]
    users[target]["primogems"] = amount
    save_data()
    await message.answer(
        f"✅ Установлено {amount} кристаллов пользователю {target}\n📊 Было: {old_gems} -> Стало: {amount}")


@dp.message(Command("create_promo"))
async def create_promo(message: types.Message):
    if message.from_user.id not in ADMINS:
        await message.answer("❌ Только для админа!")
        return

    parts = message.text.split()
    if len(parts) < 4:
        await message.answer("❌ /create_promo код награда лимит\nПример: /create_promo SEKAIGEMS 500 100")
        return

    code = parts[1].upper()
    try:
        reward = int(parts[2])
        max_uses = int(parts[3])
    except:
        await message.answer("❌ Награда и лимит должны быть числами!")
        return

    expires = None
    if len(parts) >= 5:
        try:
            days = int(parts[4])
            expires = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d %H:%M:%S")
        except:
            pass

    promocodes[code] = {"reward": reward, "uses": 0, "max_uses": max_uses, "expires": expires}
    save_data()

    expires_text = f" до {expires}" if expires else " (без срока)"
    await message.answer(
        f"✅ Промокод создан!\n🎫 Код: {code}\n💎 Награда: {reward} кристаллов\n📊 Лимит: {max_uses if max_uses > 0 else '∞'} использований{expires_text}")


@dp.message(Command("del_promo"))
async def delete_promo(message: types.Message):
    if message.from_user.id not in ADMINS:
        await message.answer("❌ Только для админа!")
        return

    parts = message.text.split()
    if len(parts) < 2:
        await message.answer("❌ /del_promo КОД")
        return

    code = parts[1].upper()
    if code not in promocodes:
        await message.answer(f"❌ Промокод {code} не найден!")
        return

    del promocodes[code]
    save_data()
    await message.answer(f"✅ Промокод {code} удален!")


@dp.message(Command("admin_logs"))
async def view_admin_logs(message: types.Message):
    if message.from_user.id not in ADMINS:
        await message.answer("❌ Только для админов!")
        return

    if not admin_logs:
        await message.answer("📭 Логи действий админов пусты")
        return

    recent_logs = admin_logs[-20:]
    text = "📋 ПОСЛЕДНИЕ ДЕЙСТВИЯ АДМИНОВ\n\n"
    for log in reversed(recent_logs):
        text += f"🕐 {log['time']}\n👤 {log['admin_name']}\n⚡ {log['action']}\n"
        if log.get('target'):
            text += f"🎯 {log['target']}\n"
        if log.get('details'):
            text += f"📝 {log['details']}\n"
        text += "\n"
    await message.answer(text[:4000])


@dp.message(Command("newusers"))
async def view_new_users(message: types.Message):
    if message.from_user.id not in ADMINS:
        await message.answer("❌ Только для админов!")
        return

    if not new_users_log:
        await message.answer("📭 Новых пользователей нет")
        return

    recent_users = new_users_log[-20:]
    text = "🆕 НОВЫЕ ПОЛЬЗОВАТЕЛИ\n\n"
    for user in reversed(recent_users):
        text += f"🕐 {user['time']}\n👤 {user['first_name']}\n🆔 {user['user_id']}\n\n"
    await message.answer(text[:4000])


# ========== АВТОМАТИЧЕСКИЙ БОНУС ==========
async def hourly_auto_bonus():
    while True:
        now = datetime.now()
        next_hour = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
        wait_seconds = (next_hour - now).total_seconds()
        await asyncio.sleep(wait_seconds)

        print(f"🕐 Выдача часовых бонусов в {datetime.now().strftime('%H:%M:%S')}")

        for user_id, data in users.items():
            bonus_amount = HOURLY_BONUS
            try:
                chat_member = await bot.get_chat_member(NEWS_CHANNEL, int(user_id))
                if chat_member.status in ["member", "creator", "administrator"]:
                    bonus_amount = HOURLY_BONUS_SUB
            except:
                pass

            users[user_id]["primogems"] += bonus_amount
            try:
                await bot.send_message(user_id,
                                       f"⏰ Ежечасный бонус!\n💎 +{bonus_amount} кристаллов\n🎰 {bonus_amount // 300} круток\n\n💎 Всего: {users[user_id]['primogems']} ({users[user_id]['primogems'] // 300} круток)")
            except:
                pass

        save_data()
        print(f"✅ Выдано бонусов {len(users)} пользователям")


async def catch_up_hourly_bonus():
    """Начисляет пропущенные часовые бонусы при запуске бота"""
    now = datetime.now()

    for user_id, data in users.items():
        last_bonus = data.get("last_hourly")

        if last_bonus:
            last_time = datetime.fromisoformat(last_bonus)
            hours_passed = (now - last_time).total_seconds() // 3600

            if hours_passed >= 1:
                # Начисляем бонусы за каждый пропущенный час
                bonus_amount = HOURLY_BONUS
                # Проверяем подписку один раз
                subscribed = False
                if CHECK_SUBSCRIPTION:
                    try:
                        chat_member = await bot.get_chat_member(NEWS_CHANNEL, int(user_id))
                        if chat_member.status in ["member", "creator", "administrator"]:
                            subscribed = True
                            bonus_amount = HOURLY_BONUS_SUB
                    except:
                        pass

                total_bonus = int(bonus_amount * hours_passed)
                users[user_id]["primogems"] += total_bonus

                # Уведомляем пользователя
                try:
                    await bot.send_message(
                        user_id,
                        f"⏰ **Бонус за время вашего отсутствия!**\n\n"
                        f"💎 +{total_bonus} кристаллов\n"
                        f"📊 За {int(hours_passed)} пропущенных часов\n\n"
                        f"💎 Всего: {users[user_id]['primogems']} ({users[user_id]['primogems'] // 300} круток)"
                    )
                except:
                    pass

        # Обновляем время последнего бонуса на текущее
        users[user_id]["last_hourly"] = now.isoformat()

    save_data()
# ========== ЗАПУСК ==========
async def main():
    load_data()
    print("=" * 50)
    print("🎴 PROJECT SEKAI ГАЧА-БОТ ЗАПУЩЕН!")
    print("=" * 50)
    print(f"👑 Админ: {ADMINS[0]}")
    print(f"📊 Пользователей: {len(users)}")
    print("=" * 50)
    print("✅ Бот готов к работе!")

    async def main():
        load_data()
        print("=" * 50)
        print("🎴 PROJECT SEKAI ГАЧА-БОТ ЗАПУЩЕН!")

        # Начисляем пропущенные бонусы
        await catch_up_hourly_bonus()

        # ... остальной код
    asyncio.create_task(hourly_auto_bonus())

    while True:
        try:
            await dp.start_polling(bot)
        except (TelegramNetworkError, ConnectionResetError) as e:
            print(f"❌ Ошибка подключения: {e}")
            print("🔄 Переподключение через 10 секунд...")
            await asyncio.sleep(10)
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            print("🔄 Перезапуск через 5 секунд...")
            await asyncio.sleep(5)


if __name__ == "__main__":
    asyncio.run(main())