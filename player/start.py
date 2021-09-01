from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup 

@Client.on_message(filters.command("start"))
async def start(client, m: Message):
   if m.chat.type == 'private':
       await m.reply(f"**I am A advanced Anime Theme VC Video Player created for playing vidio in the voice chats of Telegram Groups & Channels. \n\n**To use it:-** __ \n1) Add this Bot to your Group and Make it Admin \n2) Add__ @YuiVideoPlayer __to your Group__ \n3) **Commands** : \n`/stream` (IN REPLY TO A VIDEO) \n`/stop`",   
                            reply_markup=InlineKeyboardMarkup(
                                [[
                                     InlineKeyboardButton(
                                            "Dev", url="https://t.me/AmiFutami")
                                    ]]
                            ))
   else:
      await m.reply("**Yui is Alive! ✨**")
