from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, Chat, CallbackQuery

@Client.on_message(filters.command("start"))
async def start(client, m: Message):
   if m.chat.type == 'private':
      await m.reply(f"**Hello there 👋🏻, i'm a video stream bot, i've been created for streaming video on Group video chat.**\n\n**To know how to use me, click the help button below** 👇🏻",
                    reply_markup=InlineKeyboardMarkup(
                       [[
                          InlineKeyboardButton(
                             "❔ HOW TO USE THIS BOT", callback_data="cbguide")
                       ],[
                          InlineKeyboardButton(
                             "👩🏻‍💻 Developer", url="https://t.me/dlwrml")
                       ],[
                          InlineKeyboardButton(
                             "💭 Group", url="https://t.me/VeezSupportGroup"),
                          InlineKeyboardButton(
                             "✨ Channel", url="https://t.me/levinachannel")
                       ]]
                    ))
   else:
      await m.reply("**✨ bot is online now ✨**")
