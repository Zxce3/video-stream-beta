import os
import re
import pafy
import asyncio
from asyncio import sleep

from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls import GroupCallFactory
from youtube_dl import YoutubeDL

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
@authorized_users_only
async def vstream(_, m: Message):
    if 1 in STREAM:
        await m.reply_text(
            "😕 **sorry, there's another video streaming right now**\n\n» **wait for it to finish then try again!**")
        return

    media = m.reply_to_message
    if not media and " " not in m.text:
        await m.reply_text("🔺 **please reply to a video or live stream url or youtube url to stream the video!**")

    elif ' ' in m.text:
        msg = await m.reply_text("🔄 **processing youtube stream...**")
        text = m.text.split(' ', 1)
        query = text[1]
        regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+"
        match = re.match(regex, query)
        if match:
            await msg.edit("🔄 **starting youtube streaming...**")
            ytstreamlink = ""
            try:
                meta = ydl.extract_info(query, download=False)
                formats = meta.get('formats', [meta])
                for f in formats:
                    ytstreamlink += f['url']
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
                await msg.edit((
                                   f"💡 **started [youtube streaming]({ytstream}) !\n\n» join to video chat to watch "
                                   f"the youtube stream.**"),
                               disable_web_page_preview=True)
                try:
                    STREAM.remove(0)
                except KeyError:
                    pass
                try:
                    STREAM.add(1)
                except KeyError:
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
                await msg.edit((
                                   f"💡 **started [live streaming]({livestream}) !\n\n» join to video chat to watch "
                                   f"the live stream.**"),
                               disable_web_page_preview=True)
                try:
                    STREAM.remove(0)
                except KeyError:
                    pass
                try:
                    STREAM.add(1)
                except KeyError:
                    pass
            except Exception as e:
                await msg.edit(f"❌ **something went wrong!** \n\nerror: `{e}`")

    elif media.video or media.document:
        msg = await m.reply_text(
            "📥 **downloading video...**\n\n💭 __this process will take quite a while depending on the size of the "
            "video.__")
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
            except KeyError:
                pass
            try:
                STREAM.add(1)
            except KeyError:
                pass
        except Exception as e:
            await msg.edit(f"❌ **something went wrong!** \n\nerror: `{e}`")
    else:
        await m.reply("🔺 **please reply to a video or live stream url or youtube url to stream the video!**")
        return


@Client.on_message(command(["vstop", f"vstop@{BOT_USERNAME}"]) & filters.group & ~filters.edited)
@authorized_users_only
async def vstop(_, m: Message):
    if 0 in STREAM:
        await m.reply_text(
            "😕 **no active streaming at this time**\n\n» start streaming by using /vstream command (reply to "
            "video/yt url/live url)")
        return
    try:
        await VIDEO_CALL[m.chat.id].stop()
        await m.reply_text("🔴 **streaming has ended !**\n\n✅ __userbot has been disconnected from the video chat__")
        try:
            STREAM.remove(1)
        except KeyError:
            pass
        try:
            STREAM.add(0)
        except KeyError:
            pass
    except Exception as e:
        await m.reply_text(f"❌ **something went wrong!** \n\nerror: `{e}`")


@Client.on_message(filters.command("play"))
@authorized_users_only
async def stream(client, m: Message):
    replied = m.reply_to_message
    if not replied:
        if len(m.command) < 2:
            await m.reply("💡 reply to video or provide live stream url to start video streaming")
        else:
            video = m.text.split(None, 1)[1]
            youtube_regex = (
                                         r'(https?://)?(www\.)?'
                                       '(youtube|youtu|youtube-nocookie)\.(com|be)/'
                                       '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
            youtube_regex_match = re.match(youtube_regex, video)
            if youtube_regex_match:
            	try:
            		yt = pafy.new(video)
            		best = yt.getbest()
            		video_url = best.url
            	except Exception as e:
            		await m.reply(f"🚫 **error** - `{e}`")
            		return
            	msg = await m.reply("🔁 starting live streaming...")
            	chat_id = m.chat.id
            	await asyncio.sleep(1)
            	try:
            	   group_call = group_call_factory.get_group_call()
            	   await group_call.join(chat_id)
            	   await group_call.start_video(video_url, repeat=False)
            	   VIDEO_CALL[chat_id] = group_call
            	   await msg.edit((f"💡 **started [live streaming]({video_url}) !\n\n» join to video chat to watch streaming."), disable_web_page_preview=True)
            	except Exception as e:
            		await msg.edit(f"🚫 **error** - `{e}`")
            else:
            	msg = await m.reply("🔁 starting live streaming...")
            	chat_id = m.chat.id
            	await asyncio.sleep(1)
            	try:
            	   group_call = group_call_factory.get_group_call()
            	   await group_call.join(chat_id)
            	   await group_call.start_video(video, repeat=False)
            	   VIDEO_CALL[chat_id] = group_call
            	   await msg.edit((f"💡 **started [live streaming]({video}) !\n\n» join to video chat to watch streaming."), disable_web_page_preview=True)
            	except Exception as e:
            		await msg.edit(f"🚫 **error** - `{e}`")
            	
    elif replied.video or replied.document:
        msg = await m.reply("📥 downloading video...")
        video = await client.download_media(m.reply_to_message)
        chat_id = m.chat.id
        await asyncio.sleep(2)
        try:
            group_call = group_call_factory.get_group_call()
            await group_call.join(chat_id)
            await group_call.start_video(video, repeat=False)
            VIDEO_CALL[chat_id] = group_call
            await msg.edit("💡 **video streaming started!**\n\n» **join to video chat to watch the video.**")
        except Exception as e:
            await msg.edit(f"**🚫 error** - `{e}`")
    else:
        await m.reply("💭 please reply to video or video file to stream")


@Client.on_message(filters.command("end"))
@authorized_users_only
async def stopvideo(client, m: Message):
    chat_id = m.chat.id
    try:
        await VIDEO_CALL[chat_id].stop()
        await m.reply("✅ **streaming has ended successfully !**")
    except Exception as e:
        await m.reply(f"🚫 **error** - `{e}`")
