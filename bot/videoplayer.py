import re
from os import path
from asyncio import sleep
from youtube_dl import YoutubeDL
from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls import GroupCallFactory
from config import API_ID, API_HASH, SESSION_NAME, BOT_USERNAME
from helpers.decorators import authorized_users_only
from helpers.filters import command


STREAM = {8}
VIDEO_CALL = {}

ydl_opts = {
        "geo-bypass": True,
        "nocheckcertificate": True,
}
ydl = YoutubeDL(ydl_opts)


app = Client(
    SESSION_NAME,
    api_id=API_ID,
    api_hash=API_HASH,
)
group_call_factory = GroupCallFactory(app, GroupCallFactory.MTPROTO_CLIENT_TYPE.PYROGRAM)


@Client.on_message(command(["vstream", f"vstream@{BOT_USERNAME}"]) & filters.group & ~filters.edited)
async def vstream(_, m: Message):
    if 1 in STREAM:
        await m.reply_text("😕 **sorry, there's another video streaming right now**\n\n» **wait for it to finish then try again!**")
        return

    media = m.reply_to_message
    if not media and not ' ' in m.text:
        await m.reply_text("🔺 **please reply to a video or live stream url or youtube url to stream the video!**")

    elif ' ' in m.text:
        msg = await m.reply_text("🔄 **processing youtube stream...**")
        text = m.text.split(' ', 1)
        query = text[1]
        regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+"
        match = re.match(regex, query)
        if match:
            await msg.edit("🔄 **starting youtube streaming...**")
            try:
                meta = ydl.extract_info(query, download=False)
                formats = meta.get('formats', [meta])
                for f in formats:
                        ytstreamlink = f['url']
                ytstream = ytstreamlink
            except Exception as e:
                await msg.edit(f"❌ **youtube downloader error!** \n\n`{e}`")
                return
            await sleep(2)
            try:
                group_call = group_call_factory.get_group_call()
                await group_call.join(m.chat.id)
                await group_call.start_video(ytstream, repeat=False)
                VIDEO_CALL[m.chat.id] = group_call
                await msg.edit((f"💡 **started [youtube streaming]({ytstream}) !\n\n» join to video chat to watch the youtube stream.**"), disable_web_page_preview=True)
                try:
                    STREAM.remove(0)
                except:
                    pass
                try:
                    STREAM.add(1)
                except:
                    pass
            except Exception as e:
                await msg.edit(f"❌ **something went wrong!** \n\nError: `{e}`")
        else:
            await msg.edit("🔄 **starting live streaming...**")
            livestream = query
            await sleep(2)
            try:
                group_call = group_call_factory.get_group_call()
                await group_call.join(m.chat.id)
                await group_call.start_video(livestream, repeat=False)
                VIDEO_CALL[m.chat.id] = group_call
                await msg.edit((f"💡 **started [live streaming]({livestream}) !\n\n» join to video chat to watch the live stream.**"), disable_web_page_preview=True)
                try:
                    STREAM.remove(0)
                except:
                    pass
                try:
                    STREAM.add(1)
                except:
                    pass
            except Exception as e:
                await msg.edit(f"❌ **something went wrong!** \n\nerror: `{e}`")

    elif media.video or media.document:
        msg = await m.reply_text("📥 **downloading video...**\n\n💭 __this process will take quite a while depending on the size of the video.__")
        video = await media.download()
        await sleep(2)
        try:
            group_call = group_call_factory.get_group_call()
            await group_call.join(m.chat.id)
            await group_call.start_video(video, repeat=False)
            VIDEO_CALL[m.chat.id] = group_call
            await msg.edit("💡 **video streaming started!**\n\n» **join to video chat to watch the video.**")
            try:
                STREAM.remove(0)
            except:
                pass
            try:
                STREAM.add(1)
            except:
                pass
        except Exception as e:
            await msg.edit(f"❌ **something went wrong!** \n\nerror: `{e}`")
    else:
        await msg.edit("🔺 **please reply to a video or live stream url or youtube url to stream the video!**")
        return


@Client.on_message(command(["vstop", f"vstop@{BOT_USERNAME}"]) & filters.group & ~filters.edited)
@authorized_users_only
async def vstop(_, m: Message):
    if 0 in STREAM:
        await m.reply_text("😕 **no active streaming at this time**\n\n» start streaming by using /vstream command (reply to video/yt url/live url)")
        return
    try:
        await VIDEO_CALL[m.chat.id].stop()
        await m.reply_text("🔴 **streaming has ended !**\n\n✅ __userbot has been disconnected from the video chat__")
        try:
            STREAM.remove(1)
        except:
            pass
        try:
            STREAM.add(0)
        except:
            pass
    except Exception as e:
        await m.reply_text(f"❌ **something went wrong!** \n\nerror: `{e}`")
