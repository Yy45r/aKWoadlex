# Copyright (C) 2021 By AmortMusicProject

from driver.queues import QUEUE
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from config import (
    ASSISTANT_NAME,
    BOT_NAME,
    BOT_USERNAME,
    GROUP_SUPPORT,
    OWNER_NAME,
    UPDATES_CHANNEL,
)


@Client.on_callback_query(filters.regex("cbstart"))
async def cbstart(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""✨ **Welcome [{query.message.chat.first_name}](tg://user?id={query.message.chat.id}) !**\n
💭 **[{BOT_NAME}](https://t.me/{BOT_USERNAME}) يسمح لك بتشغيل الموسيقى والفيديو في مجموعات من خلال محادثات الفيديو الجديدة في Telegram!**

💡 **اكتشف جميع أوامر الروبوت وكيفية عملها من خلال النقر فوق » 📚 Commands button!**

🔖 **To know how to use this bot, please click on the » ❓ Basic Guide button!**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "➕أضفني إلى مجموعتك➕",
                        url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                    )
                ],
                [InlineKeyboardButton("❓دليل الأستخدام", callback_data="cbhowtouse")],
                [
                    InlineKeyboardButton("📚 الأوامر", callback_data="cbbasic"),
                    InlineKeyboardButton("❤ المالك", url=f"https://t.me/{OWNER_NAME}"),
                ],
                [
                    InlineKeyboardButton(
                        "👥 قناه الملفات", url=f"https://t.me/{GROUP_SUPPORT}"
                    ),
                    InlineKeyboardButton(
                        "📣 قناه المطور", url=f"https://t.me/{UPDATES_CHANNEL}"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "🌐 السورس", url="https://t.me/DDODD"
                    )
                ],
            ]
        ),
        disable_web_page_preview=True,
    )


@Client.on_callback_query(filters.regex("cbhowtouse"))
async def cbguides(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""🦹🏻 ** الدليل الأساسي لاستخدام هذا الروبوت:**

1.) **أولا ، أضفني إلى مجموعتك.**
2.) **بعد ذلك ، قم بترقيتي كمسؤول ومنح جميع الأذونات باستثناء التخفي.**
3.) **بعد ترقيتي ، اكتب /reload في مجموعة لتحديث بيانات المسؤول.**
3.) **أضف @{ASSISTANT_NAME} لمجموعتك أو اكتب /userbotjoin لدعوه الحساب المساعد.**
4.) ** قم بتشغيل محادثة الفيديو أولاً قبل البدء في تشغيل الفيديو / الموسيقى.**
5.) ** في بعض الأحيان ، يتم إعادة تحميل الروبوت باستخدام /reload يمكن أن يساعدك الأمر في حل بعض المشكلات.**

📌 **إذا لم ينضم المستخدم bot إلى دردشة الفيديو ، فتأكد من تشغيل دردشة الفيديو بالفعل ، أو اكتب /userbotleave ثم اكتب/userbotjoin مره اخرى.**

💡 **إذا كانت لديك أسئلة متابعة حول هذا الروبوت ، فيمكنك إخباره من خلال دردشة الدعم الخاصة بي هنا: @{GROUP_SUPPORT}**

⚡ __Powered by {BOT_NAME} __""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔻┇ رجوع", callback_data="cbstart")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbbasic"))
async def cbbasic(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""🏮هنا الأوامر الأساسية:

» /play (song name/link) -تشغيل الموسيقى على دردشة الفيديو
» /stream (query/link) - دفق الموسيقى الحية yt الحية / الراديو
» /vplay (video name/link) - تشغيل الفيديو على دردشة الفيديو
» /vstream - تشغيل فيديو مباشر من yt live / m3u8
» /playlist - تظهر لك قائمة التشغيل
» /video (query) - تحميل الفديو من اليوتيوب
» /song (query) -تحميل اغنية من اليوتيوب
» /search (query) -ابحث عن رابط فيديو youtube
» /pause - pause the stream
» /resume - استئناف التشغيل
» /skip - تخطي الاغنيه
» /stop - وقف التشغيل
» /vmute - كتم صوت المستخدم الروبوت في الدردشة الصوتية
» /vunmute - قم بإلغاء كتم صوت المستخدم الروبوت في الدردشة الصوتية
» /volume `1-200` - ضبط حجم الموسيقى (يجب أن يكون userbot مسؤولاً)
» /reload -أعد تحميل البوت وقم بتحديث بيانات المسؤول
» /userbotjoin - دعوة المستخدم الروبوت للانضمام إلى المجموعة
» /userbotleave -طلب userbot للمغادرة من المجموعة
---Sudo---
» /rmw - تنظيف جميع الملفات الخام
» /rmd - تنظيف جميع الملفات التي تم تنزيلها
» /sysinfo - عرض معلومات النظام
» /update - قم بتحديث الروبوت الخاص بك إلى أحدث إصدار
» /restart - أعد تشغيل الروبوت الخاص بك
» /leaveall - طلب userbot للمغادرة من كل المجموعة
---
» /ping - عرض حالة البوت بنك
» /uptime - عرض حالة bot الجهوزية
» /alive - عرض معلومات الروبوت على قيد الحياة (في مجموعة)

⚡️ __Powered by {BOT_NAME} __""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Go Back", callback_data="cbcmds")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbmenu"))
async def cbmenu(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("you're an Anonymous Admin !\n\n» revert back to user account from admin rights.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 المسؤول الوحيد الذي لديه إذن إدارة الدردشات الصوتية يمكنه النقر على هذا الزر !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
          await query.edit_message_text(
              f"⚙️ **settings of** {query.message.chat.title}\n\n⏸ : pause stream\n▶️ : resume stream\n🔇 : mute userbot\n🔊 : unmute userbot\n⏹ : stop stream",
              reply_markup=InlineKeyboardMarkup(
                  [[
                      InlineKeyboardButton("⏹", callback_data="cbstop"),
                      InlineKeyboardButton("⏸", callback_data="cbpause"),
                      InlineKeyboardButton("▶️", callback_data="cbresume"),
                  ],[
                      InlineKeyboardButton("🔇", callback_data="cbmute"),
                      InlineKeyboardButton("🔊", callback_data="cbunmute"),
                  ],[
                      InlineKeyboardButton("🗑 Close", callback_data="cls")],
                  ]
             ),
         )
    else:
        await query.answer("❌ لا شيء يشغل حاليا ", show_alert=True)


@Client.on_callback_query(filters.regex("cls"))
async def close(_, query: CallbackQuery):
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡المسؤول الوحيد الذي لديه إذن إدارة الدردشات الصوتية يمكنه النقر على هذا الزر!", show_alert=True)
    await query.message.delete()
