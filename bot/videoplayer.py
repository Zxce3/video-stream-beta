import os
import asyncio
from pytgcalls import GroupCallFactory
from pyrogram import Client, filters
from pyrogram.types import Message
from config import API_ID, API_HASH, SESSION_NAME

app = Client(SESSION_NAME, API_ID, API_HASH)
group_call_factory = GroupCallFactory(app, GroupCallFactory.MTPROTO_CLIENT_TYPE.PYROGRAM)
VIDEO_CALL = {}


@Client.on_message(filters.command("stream"))
async def stream(client, m: Message):
    replied = m.reply_to_message
    if not replied:
        await m.reply("😕 **sorry it's not a video**\n\n» use the /stream command by replying to the video.")
    elif replied.video or replied.document:
        msg = await m.reply("🔁 **downloading video...**\n\n❔ this process will take quite a while depending on the size of the video.")
        chat_id = m.chat.id
        try:
            video = await client.download_media(m.reply_to_message)
            await msg.edit("♻ **Converting...**")
            os.system(f'ffmpeg -i "{video}" -vn -f s16le -ac 2 -ar 48000 -acodec pcm_s16le -filter:a "atempo=0.81" vid-{chat_id}.raw -y')
        except Exception as e:
            await msg.edit(f"**🚫 Error** - `{e}`")
        await asyncio.sleep(5)
        try:
            group_call = group_call_factory.get_file_group_call(f'vid-{chat_id}.raw')
            await group_call.start(chat_id)
            await group_call.set_video_capture(video)
            VIDEO_CALL[chat_id] = group_call
            await msg.edit("**💡 video streaming started !\n\n❕ join to video chat to watch the video.**")
        except Exception as e:
            await msg.edit(f"**Error** -- `{e}`")
    else:
        await m.reply("`please reply to a video !`")

@Client.on_message(filters.command("stop"))
async def stopvideo(client, m: Message):
    chat_id = m.chat.id
    try:
        await VIDEO_CALL[chat_id].stop()
        await m.reply("**⏹️ streaming has ended !**\n\n✅ __userbot has been disconnected from the video chat__")
    except Exception as e:
        await m.reply(f"**🚫 Error** - `{e}`")
