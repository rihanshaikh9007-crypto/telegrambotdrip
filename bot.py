from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from flask import Flask
from threading import Thread
import logging
import random
import asyncio

API_TOKEN = "8694277322:AAHhDc9nS3v9EzSxrxr0POYbxOszmDW0rYQ"
ADMIN_ID = 1484173564

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

channels = []
requested_users = {}

def generate_key():
    return str(random.randint(1000000000, 9999999999))

# 🌐 WEB PANEL
@app.route('/')
def home():
    return "Bot Running 👻"

# START
@dp.message_handler(commands=['start'])
async def start(msg: types.Message):
    kb = InlineKeyboardMarkup(row_width=1)

    for ch in channels:
        kb.add(InlineKeyboardButton("JOIN CHANNEL 👻", url=f"https://t.me/{ch.replace('@','')}"))

    kb.add(InlineKeyboardButton("VERIFY ✅", callback_data="verify"))
    kb.add(InlineKeyboardButton("CLICK HERE 💀", url="https://t.me/setupchanel_0/60"))

    await bot.send_photo(
        msg.chat.id,
        photo="https://files.catbox.moe/wcfmqd.jpg",
        caption="""👻 Sab channels join karo phir VERIFY dabao

𝗛ᴇʟʟᴏ 𝗨ꜱᴇʀ 👻 𝐁𝐎𝐓

ALL CHANNEL JOIN 🥰

𝐇𝐎𝐖 𝐓𝐎 𝐆𝐄𝐍𝐄𝐑𝐀𝐓𝐄 𝐊𝐄𝐘 💀
𝐂𝐋𝐈𝐂𝐊 𝐇𝐄𝐑𝐄""",
        reply_markup=kb
    )

# JOIN REQUEST
@dp.chat_join_request_handler()
async def join_request(update: types.ChatJoinRequest):
    user_id = update.from_user.id
    chat_id = update.chat.id

    if user_id not in requested_users:
        requested_users[user_id] = []

    requested_users[user_id].append(chat_id)

    await bot.approve_chat_join_request(chat_id, user_id)

# VERIFY
@dp.callback_query_handler(lambda c: c.data == "verify")
async def verify(call: types.CallbackQuery):
    user_id = call.from_user.id

    if user_id in requested_users and len(requested_users[user_id]) >= len(channels):
        key = generate_key()

        kb = InlineKeyboardMarkup()
        kb.add(InlineKeyboardButton("OPEN TELEGRAM 🚀", url="https://t.me/+MkNcxGuk-w43MzBl"))

        await call.message.answer(f"""
Key - {key}

DRIP SCINET APK - https://www.mediafire.com/file/if3uvvwjbj87lo2/DRIPCLIENT_v6.2_GLOBAL_AP.apks/file
""", reply_markup=kb)
    else:
        await call.answer("❌ Pehle sab channel join request bhejo!", show_alert=True)

# ADMIN
@dp.message_handler(commands=['admin'])
async def admin(msg: types.Message):
    if msg.from_user.id != ADMIN_ID:
        return

    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("ADD ➕", callback_data="add"))
    kb.add(InlineKeyboardButton("REMOVE ❌", callback_data="remove"))
    kb.add(InlineKeyboardButton("TOTAL 📊", callback_data="total"))

    await msg.answer("ADMIN PANEL 👻", reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data == "add")
async def add(call: types.CallbackQuery):
    await call.message.answer("Send channel @username")
    dp.register_message_handler(save_channel)

async def save_channel(msg: types.Message):
    if msg.from_user.id != ADMIN_ID:
        return
    channels.append(msg.text)
    await msg.answer("Added")

@dp.callback_query_handler(lambda c: c.data == "remove")
async def remove(call: types.CallbackQuery):
    await call.message.answer("Send channel to remove")
    dp.register_message_handler(delete_channel)

async def delete_channel(msg: types.Message):
    if msg.text in channels:
        channels.remove(msg.text)
        await msg.answer("Removed")

@dp.callback_query_handler(lambda c: c.data == "total")
async def total(call: types.CallbackQuery):
    await call.message.answer(f"Total: {len(channels)}")

# BOT THREAD
def start_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    executor.start_polling(dp, skip_updates=True)

# MAIN
if __name__ == "__main__":
    Thread(target=start_bot).start()
    app.run(host="0.0.0.0", port=10000)
