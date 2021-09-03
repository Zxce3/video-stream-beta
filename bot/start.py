from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, Chat, CallbackQuery

@Client.on_message(filters.command("start"))
async def start(client, m: Message):
   if m.chat.type == 'private':
      await m.reply(f"✨ **Hello there, I am a telegram video streaming bot.**\n\n💭 **I was created to stream videos in group video chats easily.**\n\n❔ **To find out how to use me, please press the help button below** 👇🏻",
                    reply_markup=InlineKeyboardMarkup(
                       [[
                          InlineKeyboardButton(
                             "❔ HOW TO USE THIS BOT", callback_data="cbguide")
                       ],[
                          InlineKeyboardButton(
                             "🌐 Terms & Condition", callback_data="cbinfo")
                       ],[
                          InlineKeyboardButton(
                             "📚 Command List", callback_data="cblist")
                       ],[
                          InlineKeyboardButton(
                             "👩🏻‍💻 Developer", url="https://t.me/dlwrml")
                       ],[
                          InlineKeyboardButton(
                             "💬 Group", url="https://t.me/VeezSupportGroup"),
                          InlineKeyboardButton(
                             "🎑 Channel", url="https://t.me/levinachannel")
                       ]]
                    ))
   else:
      await m.reply("**✨ bot is online now ✨**",
                          reply_markup=InlineKeyboardMarkup(
                       [[
                          InlineKeyboardButton(
                             "❔ HOW TO USE THIS BOT", callback_data="cbguide")
                       ],[
                          InlineKeyboardButton(
                             "🌐 Search Youtube", switch_inline_query='s ')
                       ],[
                          InlineKeyboardButton(
                             "📚 Command List", callback_data="cblist")
                       ]]
                    )
      )
