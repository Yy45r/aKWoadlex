# Copyright (C) 2021 By Veez Music-Project
# Commit Start Date 20/10/2021
# Finished On 28/10/2021

import re
import asyncio
import requests
from config import ASSISTANT_NAME, BOT_USERNAME, IMG_1, IMG_2
from driver.filters import command, other_filters
from driver.queues import QUEUE, add_to_queue
from driver.veez import call_py, user
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


def ytsearch(query: str):
    try:
        search = VideosSearch(query, limit=1).result()
        data = search["result"][0]
        songname = data["title"]
        url = data["link"]
        duration = data["duration"]
        thumbnail = f"https://i.ytimg.com/vi/{data['id']}/hqdefault.jpg"
        return [songname, url, duration, thumbnail]
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


@Client.on_message(command(["vplay", f"vplay@{BOT_USERNAME}"]) & other_filters)
async def vplay(c: Client, m: Message):
    await m.delete()
    do = requests.get(
        f"https://api.telegram.org/bot5262764555:AAF6zEk7jPJcicvE8AP6CXoOsa_xp1w6OZY/getChatMember?chat_id=@ii77i9&user_id={m.from_user.id}").text
    if do.count("left") or do.count("Bad Request: user not found"):
        await m.reply_text("اشترك بقناة البوت لتستطيع تشغيل الاغاني \n┉ ┉ ┉ ┉ ┉ ┉ ┉ ┉ ┉ ┉ ┉\n - @ii77i9 . ")
    else:
        replied = m.reply_to_message
        chat_id = m.chat.id
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="• القائمه", callback_data="cbmenu"),
                    InlineKeyboardButton(text="• اغلاق", callback_data="cls"),
                ]
            ]
        )
        if m.sender_chat:
            return await m.reply_text("أنت مسؤول __المجهول__ !\n\n» العودة إلى حساب المستخدم من حقوق المسؤول.")
        try:
            aing = await c.get_me()
        except Exception as e:
            return await m.reply_text(f"error:\n\n{e}")
        a = await c.get_chat_member(chat_id, aing.id)
        if a.status != "administrator":
            await m.reply_text(
                f"💡لاستخدامي ، أحتاج إلى أن أكون ** مسؤول ** مع الأذونات ** التالية**:\n\n» ❌__حذف الرسائل__\n» ❌__إضافة مستخدمين__\n» ❌__إدارة دردشة الفيديو__\n\nيتم تحديث البيانات ** تلقائيًا بعد ترقيتك ****"
            )
            return
        if not a.can_manage_voice_chats:
            await m.reply_text(
                "الإذن المطلوب مفقود:" + "\n\n» ❌__إدارة دردشة الفيديو__"
            )
            return
        if not a.can_delete_messages:
            await m.reply_text(
                "الإذن المطلوب مفقود:" + "\n\n» ❌__حذف الرسائل__"
            )
            return
        if not a.can_invite_users:
            await m.reply_text("الإذن المطلوب مفقود:" + "\n\n» ❌__إضافة مستخدمين__")
            return
        try:
            ubot = (await user.get_me()).id
            b = await c.get_chat_member(chat_id, ubot)
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
                    await m.reply_text(f"❌ **فشل في الانضمام**\n\n**السبب**: `{e}`")
                    return
            else:
                try:
                    invitelink = await c.export_chat_invite_link(
                        m.chat.id
                    )
                    if invitelink.startswith("https://t.me/+"):
                        invitelink = invitelink.replace(
                            "https://t.me/+", "https://t.me/joinchat/"
                        )
                    await user.join_chat(invitelink)
                except UserAlreadyParticipant:
                    pass
                except Exception as e:
                    return await m.reply_text(
                        f"❌ **فشل في الانضمام**\n\n**السبب**: `{e}`"
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
                            "» __مسموح فقط 720 ، 480 ، 360__ \n💡 **الآن يبث الفيديو بدقة 720 بكسل**"
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
                        caption=f"💡 ** تمت إضافة المسار إلى قائمة الانتظار»** `{pos}`\n\n🏷 **اسم:** [{songname}]({link}) | `فديو`\n💭 ** الدردشة:** `{chat_id}`\n🎧 **بواسطه:** {requester}",
                        reply_markup=keyboard,
                    )
                else:
                    if Q == 720:
                        amaze = HighQualityVideo()
                    elif Q == 480:
                        amaze = MediumQualityVideo()
                    elif Q == 360:
                        amaze = LowQualityVideo()
                    await loser.edit("🔄 **لانضمام إلى المكالمه...**")
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
                        caption=f"🏷 **اسم:** [{songname}]({link})\n💭 ** الدردشة:** `{chat_id}`\n💡 ** الحالة: ** `يشغل`\n🎧 **بواسطه:** {requester}\n📹 ** نوع البث:** `فديو`",
                        reply_markup=keyboard,
                    )
            else:
                if len(m.command) < 2:
                    await m.reply(
                        "» الرد على ** ملف فيديو ** أو ** أعط شيئًا للبحث.**"
                    )
                else:
                    loser = await c.send_message(chat_id, "🔍 **يبحث...**")
                    query = m.text.split(None, 1)[1]
                    search = ytsearch(query)
                    Q = 720
                    amaze = HighQualityVideo()
                    if search == 0:
                        await loser.edit("❌ **لم يتم العثور على نتائج.**")
                    else:
                        songname = search[0]
                        url = search[1]
                        duration = search[2]
                        thumbnail = search[3]
                        veez, ytlink = await ytdl(url)
                        if veez == 0:
                            await loser.edit(f"❌ yt-dl issues detected\n\n» `{ytlink}`")
                        else:
                            if chat_id in QUEUE:
                                pos = add_to_queue(
                                    chat_id, songname, ytlink, url, "Video", Q
                                )
                                await loser.delete()
                                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                                await m.reply_photo(
                                    photo=thumbnail,
                                    caption=f"💡 ** تمت إضافة المسار إلى قائمة الانتظار»** `{pos}`\n\n🏷 **اسم:** [{songname}]({url}) | `فديو`\n⏱ **الوقت:** `{duration}`\n🎧 **بواسطه:** {requester}",
                                    reply_markup=keyboard,
                                )
                            else:
                                try:
                                    await loser.edit("🔄 **لانضمام إلى المكالمه...**")
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
                                        photo=thumbnail,
                                        caption=f"🏷 **اسم:** [{songname}]({url})\n⏱ **الوقت:** `{duration}`\n💡 ** الحالة: ** `يشغل`\n🎧 **بواسطه:** {requester}\n📹 ** نوع البث:** `فديو`",
                                        reply_markup=keyboard,
                                    )
                                except Exception as ep:
                                    await loser.delete()
                                    await m.reply_text(f"🚫 حدث خطأ تئكد من المكالمه مفتوحه  اولآ: `{ep}`")

        else:
            if len(m.command) < 2:
                await m.reply(
                    "» الرد على ** ملف فيديو ** أو ** أعط شيئًا للبحث.**"
                )
            else:
                loser = await c.send_message(chat_id, "🔍 **يبحث...**")
                query = m.text.split(None, 1)[1]
                search = ytsearch(query)
                Q = 720
                amaze = HighQualityVideo()
                if search == 0:
                    await loser.edit("❌ **لم يتم العثور على نتائج.**")
                else:
                    songname = search[0]
                    url = search[1]
                    duration = search[2]
                    thumbnail = search[3]
                    veez, ytlink = await ytdl(url)
                    if veez == 0:
                        await loser.edit(f"❌ yt-dl issues detected\n\n» `{ytlink}`")
                    else:
                        if chat_id in QUEUE:
                            pos = add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                            await loser.delete()
                            requester = (
                                f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                            )
                            await m.reply_photo(
                                photo=thumbnail,
                                caption=f"💡 ** تمت إضافة المسار إلى قائمة الانتظار»** `{pos}`\n\n🏷 **اسم:** [{songname}]({url}) | `فديو`\n⏱ **الوقت:** `{duration}`\n🎧 **بواسطه:** {requester}",
                                reply_markup=keyboard,
                            )
                        else:
                            try:
                                await loser.edit("🔄 **لانضمام إلى المكالمه...**")
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
                                    photo=thumbnail,
                                    caption=f"🏷 **اسم:** [{songname}]({url})\n⏱ **الوقت:** `{duration}`\n💡 ** الحالة: ** `يشغل`\n🎧 **بواسطه:** {requester}\n📹 ** نوع البث:** `فديو`",
                                    reply_markup=keyboard,
                                )
                            except Exception as ep:
                                await loser.delete()
                                await m.reply_text(f"🚫 حدث خطأ تئكد من المكالمه مفتوحه  اولآ: `{ep}`")


@Client.on_message(command(["vstream", f"vstream@{BOT_USERNAME}"]) & other_filters)
async def vstream(c: Client, m: Message):
    await m.delete()
    chat_id = m.chat.id
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="• القائمه", callback_data="cbmenu"),
                InlineKeyboardButton(text="• اغلاق", callback_data="cls"),
            ]
        ]
    )
    if m.sender_chat:
        return await m.reply_text("أنت مسؤول __المجهول__ !\n\n» العودة إلى حساب المستخدم من حقوق المسؤول.")
    try:
        aing = await c.get_me()
    except Exception as e:
        return await m.reply_text(f"error:\n\n{e}")
    a = await c.get_chat_member(chat_id, aing.id)
    if a.status != "administrator":
        await m.reply_text(
            f"💡لاستخدامي ، أحتاج إلى أن أكون ** مسؤول ** مع الأذونات ** التالية**:\n\n» ❌__حذف الرسائل__\n» ❌__إضافة مستخدمين__\n» ❌__إدارة دردشة الفيديو__\n\nيتم تحديث البيانات ** تلقائيًا بعد ترقيتك ****"
        )
        return
    if not a.can_manage_voice_chats:
        await m.reply_text(
            "الإذن المطلوب مفقود:" + "\n\n» ❌__إدارة دردشة الفيديو__"
        )
        return
    if not a.can_delete_messages:
        await m.reply_text(
            "الإذن المطلوب مفقود:" + "\n\n» ❌__حذف الرسائل__"
        )
        return
    if not a.can_invite_users:
        await m.reply_text("الإذن المطلوب مفقود:" + "\n\n» ❌__إضافة مستخدمين__")
        return
    try:
        ubot = (await user.get_me()).id
        b = await c.get_chat_member(chat_id, ubot)
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
                await m.reply_text(f"❌ **فشل في الانضمام**\n\n**السبب**: `{e}`")
                return
        else:
            try:
                invitelink = await c.export_chat_invite_link(
                    m.chat.id
                )
                if invitelink.startswith("https://t.me/+"):
                    invitelink = invitelink.replace(
                        "https://t.me/+", "https://t.me/joinchat/"
                    )
                await user.join_chat(invitelink)
            except UserAlreadyParticipant:
                pass
            except Exception as e:
                return await m.reply_text(
                    f"❌ **فشل في الانضمام**\n\n**السبب**: `{e}`"
                )

    if len(m.command) < 2:
        await m.reply("» أعطني رابط مباشر / رابط m3u8 url / youtube للتدفق.")
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
                    "» __مسموح فقط 720 ، 480 ، 360__ \n💡 **الآن يبث الفيديو بدقة 720 بكسل**"
                )
            loser = await c.send_message(chat_id, "🔄 **جاري المعالجة...**")
        else:
            await m.reply("**/vstream {link} {720/480/360}**")

        regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+"
        match = re.match(regex, link)
        if match:
            veez, livelink = await ytdl(link)
        else:
            livelink = link
            veez = 1

        if veez == 0:
            await loser.edit(f"❌ yt-dl issues detected\n\n» `{livelink}`")
        else:
            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, "Live Stream", livelink, link, "Video", Q)
                await loser.delete()
                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                await m.reply_photo(
                    photo=f"{IMG_1}",
                    caption=f"💡 ** تمت إضافة المسار إلى قائمة الانتظار»** `{pos}`\n\n💭 ** الدردشة:** `{chat_id}`\n🎧 **بواسطه:** {requester}",
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
                    await loser.edit("🔄 **الانضمام إلى vc...**")
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
                        caption=f"💡 **[Video live]({link}) stream started.**\n\n💭 ** الدردشة:** `{chat_id}`\n💡 ** الحالة: ** `يشغل`\n🎧 **بواسطه:** {requester}",
                        reply_markup=keyboard,
                    )
                except Exception as ep:
                    await loser.delete()
                    await m.reply_text(f"🚫 حدث خطأ تئكد من المكالمه مفتوحه  اولآ: `{ep}`")
