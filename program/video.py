# Copyright (C) 2021 By Amort Music-Project
# Commit Start Date 20/10/2021
# Finished On 28/10/2021

import re
import asyncio
import json
import urllib
from config import ASSISTANT_NAME, BOT_USERNAME, IMG_1, IMG_2
from driver.filters import command, other_filters
from driver.queues import QUEUE, add_to_queue
from driver.amort import call_py, user
from pyrogram import Client
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioVideoPiped
from pytgcalls.types.input_stream.quality import (
    HighQualityAudio,
    HighQualityVideo,
    LowQualityVideo,
    MediumQualityVideo,
)
from youtubesearchpython import VideosSearch


def ytsearch(query):
    try:
        search = VideosSearch(query, limit=1)
        for r in search.result()["result"]:
            ytid = r["id"]
            if len(r["title"]) > 34:
                songname = r["title"][:70]
            else:
                songname = r["title"]
            url = f"https://www.youtube.com/watch?v={ytid}"
        return [songname, url]
    except Exception as e:
        print(e)
        return 0


async def ytdl(link):
    proc = await asyncio.create_subprocess_exec(
        "yt-dlp",
        "-g",
        "-f",
        "best[height<=?720][width<=?1280]",
        f"{link}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if stdout:
        return 1, stdout.decode().split("\n")[0]
    else:
        return 0, stderr.decode()


@Client.on_message(command(["playv", f"playv@{BOT_USERNAME}"]) & other_filters)
async def vplay(c: Client, m: Message):
    replied = m.reply_to_message
    chat_id = m.chat.id
    idd = m.from_user.id
    ch = "b666P"
    res = urllib.urlopen("https://api.telegram.org/bot{}/getChatMember?chat_id={}&user_id={}".format(Client,ch,idd)).read()
    o = json.loads(res)
    r = o['reslt']['status']
    if r == 'left':
        await m.reply_text('عذرأ عزيزي عليك الاشتراك في قناة البوت اولا \n {}'.format(ch))
    else:
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="• Mᴇɴᴜ", callback_data="cbmenu"),
                    InlineKeyboardButton(text="• Cʟᴏsᴇ", callback_data="cls"),
                ]
            ]
        )
        if m.sender_chat:
            return await m.reply_text("أنت __مسؤول مجهول__ !\n\n» ارجع إلى حساب المستخدم من حقوق المسؤول.")
        try:
            aing = await c.get_me()
        except Exception as e:
            return await m.reply_text(f"error:\n\n{e}")
        a = await c.get_chat_member(chat_id, aing.id)
        if a.status != "administrator":
            await m.reply_text(
                f"💡لاستخدامي ، أحتاج إلى أن أكون ** مسؤول ** مع ما يلي**:\n\n» ❌ __حذف الرسائل__\n» ❌ __أضف المستخدمين__\n» ❌ __إدارة دردشة الفيديو__\n\nيتم تحديث البيانات ** تلقائيًا بعد ترقيتك ****"
            )
            return
        if not a.can_manage_voice_chats:
            await m.reply_text(
                "missing required permission:" + "\n\n» ❌ _إدارة دردشة الفيديو__"
            )
            return
        if not a.can_delete_messages:
            await m.reply_text(
                "missing required permission:" + "\n\n» ❌ __حذف الرسائل__"
            )
            return
        if not a.can_invite_users:
            await m.reply_text("missing required permission:" + "\n\n» ❌ __ضف المستخدمين__")
            return
        try:
            ubot = await user.get_me()
            b = await c.get_chat_member(chat_id, ubot.id)
            if b.status == "kicked":
                await m.reply_text(
                    f"@{ASSISTANT_NAME} **محظور في المجموعة** {m.chat.title}\n\n» **قم بفك حظر المستخدم أولاً إذا كنت تريد استخدام هذا الروبوت.**"
                )
                return
        except UserNotParticipant:
            if m.chat.username:
                try:
                    await user.join_chat(m.chat.username)
                except Exception as e:
                    await m.reply_text(f"❌ *فشل البوت في الانضمام**\n\n**السبب**: `{e}`")
                    return
            else:
                try:
                    pope = await c.export_chat_invite_link(chat_id)
                    pepo = await c.revoke_chat_invite_link(chat_id, pope)
                    await user.join_chat(pepo.invite_link)
                except UserAlreadyParticipant:
                    pass
                except Exception as e:
                    return await m.reply_text(
                        f"❌ **فشل البوت في الانضمام**\n\n**السبب**: `{e}`"
                    )

        if replied:
            if replied.video or replied.document:
                loser = await replied.reply("📥 **تحميل الفيديو...**")
                dl = await replied.download()
                link = replied.link
                if len(m.command) < 2:
                    Q = 720
                else:
                    pq = m.text.split(None, 1)[1]
                    if pq == "720" or "480" or "360":
                        Q = int(pq)
                    else:
                        Q = 720
                        await loser.edit(
                            "» __only 720, 480, 360 allowed__ \n💡 * الآن يتدفقون الفيديو بدقة 720 بكسل**"
                        )
                try:
                    if replied.video:
                        songname = replied.video.file_name[:70]
                    elif replied.document:
                        songname = replied.document.file_name[:70]
                except BaseException:
                    songname = "Video"

                if chat_id in QUEUE:
                    pos = add_to_queue(chat_id, songname, dl, link, "Video", Q)
                    await loser.delete()
                    requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                    await m.reply_photo(
                        photo=f"{IMG_1}",
                        caption=f"💡 **تمت إضافة المسار إلى قائمة الانتظار »** `{pos}`\n\n🏷 **الاسم:** [{songname}]({link})\n💭 **الدردشه:** `{chat_id}`\n🎧 **بواسطه:** {requester}",
                        reply_markup=keyboard,
                    )
                else:
                    if Q == 720:
                        amaze = HighQualityVideo()
                    elif Q == 480:
                        amaze = MediumQualityVideo()
                    elif Q == 360:
                        amaze = LowQualityVideo()
                    await loser.edit("🔄 **انضمام vc...**")
                    await call_py.join_group_call(
                        chat_id,
                        AudioVideoPiped(
                            dl,
                            HighQualityAudio(),
                            amaze,
                        ),
                        stream_type=StreamType().local_stream,
                    )
                    add_to_queue(chat_id, songname, dl, link, "Video", Q)
                    await loser.delete()
                    requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                    await m.reply_photo(
                        photo=f"{IMG_2}",
                        caption=f"💡 **بدأ تشغيل الفيديو.**\n\n🏷 **الاسم:** [{songname}]({link})\n💭 **الدردشه:** `{chat_id}`\n💡 **Status:** `يشغل`\n🎧 **بواسطه:** {requester}",
                        reply_markup=keyboard,
                    )
            else:
                if len(m.command) < 2:
                    await m.reply(
                        "»الرد على ** ملف فيديو ** أو ** أعط شيئًا للبحث**"
                    )
                else:
                    loser = await c.send_message(chat_id, "🔎 **يبحث...**")
                    query = m.text.split(None, 1)[1]
                    search = ytsearch(query)
                    Q = 720
                    amaze = HighQualityVideo()
                    if search == 0:
                        await loser.edit("❌ *م يتم العثور على نتائج.**")
                    else:
                        songname = search[0]
                        url = search[1]
                        amort, ytlink = await ytdl(url)
                        if amort == 0:
                            await loser.edit(f"❌ تم اكتشاف مشكلات yt-dl\n\n» `{ytlink}`")
                        else:
                            if chat_id in QUEUE:
                                pos = add_to_queue(
                                    chat_id, songname, ytlink, url, "Video", Q
                                )
                                await loser.delete()
                                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                                await m.reply_photo(
                                    photo=f"{IMG_1}",
                                    caption=f"💡 **تمت إضافة المسار إلى قائمة الانتظار »** `{pos}`\n\n🏷 **الاسم:** [{songname}]({url})\n💭 **الدردشه:** `{chat_id}`\n🎧 **بواسطه:** {requester}",
                                    reply_markup=keyboard,
                                )
                            else:
                                try:
                                    await loser.edit("🔄 **الانضمام إلى vc...**")
                                    await call_py.join_group_call(
                                        chat_id,
                                        AudioVideoPiped(
                                            ytlink,
                                            HighQualityAudio(),
                                            amaze,
                                        ),
                                        stream_type=StreamType().local_stream,
                                    )
                                    add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                                    await loser.delete()
                                    requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                                    await m.reply_photo(
                                        photo=f"{IMG_2}",
                                        caption=f"💡 ** بدأ تشغيل الفيديو.**\n\n🏷 **الاسم:** [{songname}]({url})\n💭 **الدردشه:** `{chat_id}`\n💡 **الحاله:** `يشغل`\n🎧 **بواسطه:** {requester}",
                                        reply_markup=keyboard,
                                    )
                                except Exception as ep:
                                    await loser.delete()
                                    await m.reply_text(f"🚫 خطأ: `{ep}`")

        else:
            if len(m.command) < 2:
                await m.reply(
                    "» الرد على ** ملف فيديو** or **إعطاء شيء للبحث.**"
                )
            else:
                loser = await c.send_message(chat_id, "🔎 **يبحث...**")
                query = m.text.split(None, 1)[1]
                search = ytsearch(query)
                Q = 720
                amaze = HighQualityVideo()
                if search == 0:
                    await loser.edit("❌ **لم يتم العثور على نتائج.**")
                else:
                    songname = search[0]
                    url = search[1]
                    amort, ytlink = await ytdl(url)
                    if amort == 0:
                        await loser.edit(f"❌تم اكتشاف مشكلات yt-dl\n\n» `{ytlink}`")
                    else:
                        if chat_id in QUEUE:
                            pos = add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                            await loser.delete()
                            requester = (
                                f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                            )
                            await m.reply_photo(
                                photo=f"{IMG_1}",
                                caption=f"💡 **تمت إضافة المسار إلى قائمة الانتظار »** `{pos}`\n\n🏷 **الاسم:** [{songname}]({url})\n💭 **دردشة:** `{chat_id}`\n🎧 **بواسطه:** {requester}",
                                reply_markup=keyboard,
                            )
                        else:
                            try:
                                await loser.edit("🔄 **انضمام vc...**")
                                await call_py.join_group_call(
                                    chat_id,
                                    AudioVideoPiped(
                                        ytlink,
                                        HighQualityAudio(),
                                        amaze,
                                    ),
                                    stream_type=StreamType().local_stream,
                                )
                                add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                                await loser.delete()
                                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                                await m.reply_photo(
                                    photo=f"{IMG_2}",
                                    caption=f"💡 **بدأ تشغيل الفيديو.**\n\n🏷 **الاسم:** [{songname}]({url})\n💭 **الدردشه:** `{chat_id}`\n💡 **الحاله:** `يشغل`\n🎧 *بواسطه:** {requester}",
                                    reply_markup=keyboard,
                                )
                            except Exception as ep:
                                await loser.delete()
                                await m.reply_text(f"🚫 خطأ: `{ep}`")


@Client.on_message(command(["vstream", f"vstream@{BOT_USERNAME}"]) & other_filters)
async def vstream(c: Client, m: Message):
    m.reply_to_message
    chat_id = m.chat.id
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="• Mᴇɴᴜ", callback_data="cbmenu"),
                InlineKeyboardButton(text="• Cʟᴏsᴇ", callback_data="cls"),
            ]
        ]
    )
    if m.sender_chat:
        return await m.reply_text("أنت مسؤول __مجهول__ !\n\n» العودة إلى حساب المستخدم من حقوق المسؤول.")
    try:
        aing = await c.get_me()
    except Exception as e:
        return await m.reply_text(f"error:\n\n{e}")
    a = await c.get_chat_member(chat_id, aing.id)
    if a.status != "administrator":
        await m.reply_text(
            f"💡 لاستخدامي ، أحتاج إلى أن أكون ** مسؤول ** مع الأذونات ** التالية**:\n\n» ❌ __حذف الرسائل__\n» ❌ __ضف المستخدمين__\n» ❌ __إدارة دردشة الفيديو__\n\nيتم تحديث البيانات ** تلقائيًا بعد ترقيتك ****"
        )
        return
    if not a.can_manage_voice_chats:
        await m.reply_text(
            "missing required permission:" + "\n\n» ❌ __إدارة دردشة الفيديو__"
        )
        return
    if not a.can_delete_messages:
        await m.reply_text(
            "missing required permission:" + "\n\n» ❌ __حذف الرسائلs__"
        )
        return
    if not a.can_invite_users:
        await m.reply_text("missing required permission:" + "\n\n» ❌ __ضف المستخدمين__")
        return
    try:
        ubot = await user.get_me()
        b = await c.get_chat_member(chat_id, ubot.id)
        if b.status == "kicked":
            await m.reply_text(
                f"@{ASSISTANT_NAME} **محظور في المجموعة** {m.chat.title}\n\n» **قم بفك حظر المستخدم أولاً إذا كنت تريد استخدام هذا الروبوت.**"
            )
            return
    except UserNotParticipant:
        if m.chat.username:
            try:
                await user.join_chat(m.chat.username)
            except Exception as e:
                await m.reply_text(f"❌ ** فشل البوت في الانضمام**\n\n**reason**: `{e}`")
                return
        else:
            try:
                pope = await c.export_chat_invite_link(chat_id)
                pepo = await c.revoke_chat_invite_link(chat_id, pope)
                await user.join_chat(pepo.invite_link)
            except UserAlreadyParticipant:
                pass
            except Exception as e:
                return await m.reply_text(
                    f"❌ **فشل لبوت في الانضمام**\n\n**reason**: `{e}`"
                )

    if len(m.command) < 2:
        await m.reply("» أعطني رابط مباشر / رابط m3u8 url / youtube للتشغيل..")
    else:
        if len(m.command) == 2:
            link = m.text.split(None, 1)[1]
            Q = 720
            loser = await c.send_message(chat_id, "🔄 **جاري المعالجة...**")
        elif len(m.command) == 3:
            op = m.text.split(None, 1)[1]
            link = op.split(None, 1)[0]
            quality = op.split(None, 1)[1]
            if quality == "720" or "480" or "360":
                Q = int(quality)
            else:
                Q = 720
                await m.reply(
                    "» __only 720, 480, 360 allowed__ \n💡 **لآن يشغل الفيديو بدقة 720 بكسل**"
                )
            loser = await c.send_message(chat_id, "🔄 **جاري المعالجة...**")
        else:
            await m.reply("**/vstream {link} {720/480/360}**")

        regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+"
        match = re.match(regex, link)
        if match:
            amort, livelink = await ytdl(link)
        else:
            livelink = link
            amort = 1

        if amort == 0:
            await loser.edit(f"❌تم اكتشاف مشكلات yt-dl\n\n» `{livelink}`")
        else:
            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, "Live Stream", livelink, link, "Video", Q)
                await loser.delete()
                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                await m.reply_photo(
                    photo=f"{IMG_1}",
                    caption=f"💡 **تمت إضافة المسار إلى قائمة الانتظار »** `{pos}`\n\n💭 **الدردشه:** `{chat_id}`\n🎧 **بواسطه:** {requester}",
                    reply_markup=keyboard,
                )
            else:
                if Q == 720:
                    amaze = HighQualityVideo()
                elif Q == 480:
                    amaze = MediumQualityVideo()
                elif Q == 360:
                    amaze = LowQualityVideo()
                try:
                    await loser.edit("🔄 **انضمام vc...**")
                    await call_py.join_group_call(
                        chat_id,
                        AudioVideoPiped(
                            livelink,
                            HighQualityAudio(),
                            amaze,
                        ),
                        stream_type=StreamType().live_stream,
                    )
                    add_to_queue(chat_id, "Live Stream", livelink, link, "Video", Q)
                    await loser.delete()
                    requester = (
                        f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                    )
                    await m.reply_photo(
                        photo=f"{IMG_2}",
                        caption=f"💡 **[فيديو مباشر]({link}) بدأ التشغيل.**\n\n💭 **الدردشه:** `{chat_id}`\n💡 **الحاله:** `يشغل`\n🎧 **بواسطه:** {requester}",
                        reply_markup=keyboard,
                    )
                except Exception as ep:
                    await loser.delete()
                    await m.reply_text(f"🚫 خطأ: `{ep}`")
