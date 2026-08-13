import asyncio
import json
import logging
import os
import re
from datetime import datetime

from telethon import events, functions

LOGS = logging.getLogger(__name__)

# ملف حفظ بيانات الحماية
DATA_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "pmpermit_data.json",
)

MAX_FLOOD_IN_PMS = int(os.getenv("MAX_FLOOD_IN_PMS", "6"))
BOTLOG_CHATID = os.getenv("BOTLOG_CHATID")

# حالات الحماية داخل هذا الحساب
state = {
    "enabled": False,
    "pmwarns": {},
    "message_cache": {},
    "approved": {},
    "temporary_approved": [],
}


def _load():
    global state
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict):
                state.update(data)
    except Exception as e:
        LOGS.warning("تعذر تحميل بيانات الحماية: %s", e)


def _save():
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
    except Exception as e:
        LOGS.warning("تعذر حفظ بيانات الحماية: %s", e)


def _mention(user):
    name = getattr(user, "first_name", None) or "المستخدم"
    return f"[{name}](tg://user?id={user.id})"


async def _edit_delete(event, text, delay=5):
    try:
        await event.edit(text)
    except Exception:
        try:
            msg = await event.reply(text)
            await asyncio.sleep(delay)
            await msg.delete()
            return
        except Exception:
            return

    await asyncio.sleep(delay)
    try:
        await event.delete()
    except Exception:
        pass


async def _edit_or_reply(event, text):
    try:
        await event.edit(text)
    except Exception:
        await event.reply(text)


async def _get_target(event, text):
    # الرد على رسالة
    if event.is_reply:
        try:
            reply = await event.get_reply_message()
            if reply and reply.sender_id:
                return await event.client.get_entity(reply.sender_id), text
        except Exception:
            pass

    # معرف أو ID داخل الأمر
    value = (text or "").strip()
    if not value:
        if event.is_private:
            try:
                return await event.get_chat(), ""
            except Exception:
                return None, ""
        return None, ""

    value = value.split()[0]

    try:
        if value.lstrip("-").isdigit():
            return await event.client.get_entity(int(value)), " ".join(
                (text or "").split()[1:]
            )
        return await event.client.get_entity(value), " ".join(
            (text or "").split()[1:]
        )
    except Exception:
        return None, text


def _approved(user_id):
    return str(user_id) in state["approved"]


def _temp_approved(user_id):
    return int(user_id) in state["temporary_approved"]


def _remove_from_temp_lists(user_id):
    uid = int(user_id)
    state["temporary_approved"] = [
        x for x in state["temporary_approved"] if int(x) != uid
    ]


async def _clear_cached_message(event, user_id):
    key = str(user_id)
    msg_id = state["message_cache"].get(key)
    if not msg_id:
        return

    try:
        await event.client.delete_messages(user_id, msg_id)
    except Exception as e:
        LOGS.info(str(e))

    state["message_cache"].pop(key, None)
    _save()


async def _log_action(event, text):
    if not BOTLOG_CHATID:
        return
    try:
        await event.client.send_message(int(BOTLOG_CHATID), text)
    except Exception as e:
        LOGS.info("تعذر إرسال سجل الحماية: %s", e)


async def _block_user(event, user):
    try:
        await event.client(functions.contacts.BlockRequest(user.id))
    except Exception as e:
        LOGS.warning("تعذر حظر %s: %s", user.id, e)


async def _unblock_user(event, user):
    try:
        await event.client(functions.contacts.UnblockRequest(user.id))
    except Exception as e:
        LOGS.warning("تعذر إلغاء حظر %s: %s", user.id, e)


async def _private_protection(event):
    if not state["enabled"]:
        return

    if not event.is_private or not event.incoming:
        return

    user = await event.get_sender()
    if not user or getattr(user, "bot", False):
        return

    uid = str(user.id)

    if _approved(user.id) or _temp_approved(user.id):
        return

    warns = int(state["pmwarns"].get(uid, 0)) + 1

    if warns > MAX_FLOOD_IN_PMS:
        state["pmwarns"].pop(uid, None)
        await _clear_cached_message(event, user.id)
        _save()

        await event.reply(
            "**⤶ لقـد حذرتـڪ مـسـبـقًـا مـن الـتـڪـرار 📵**\n"
            "**⤶ تـم حـظـرڪ تلقـائيـاً .. الان لا يـمـڪـنـڪ ازعـاجـي 🔕**"
        )

        await _block_user(event, user)

        await _log_action(
            event,
            f"#حمـايـة_الخـاص\n"
            f"**المستخدم:** {_mention(user)}\n"
            f"**الـID:** `{user.id}`\n"
            f"**تم حظره تلقائياً.**\n"
            f"**عدد الرسائل:** {warns}",
        )
        return

    state["pmwarns"][uid] = warns

    me = await event.client.get_me()
    mention = _mention(user)
    my_name = getattr(me, "first_name", None) or "المالك"
    total = MAX_FLOOD_IN_PMS + 1
    remaining = max(total - warns, 0)

    text = (
        "**━ 𝐀𝐔𝐓𝐎 𝐑𝐄𝐏𝐋𝐘 - الرد الآلــي 💪**\n"
        "**•─────────────────•**\n\n"
        f"❞ **مرحبًـا** {mention} ❝\n\n"
        f"**⤶ قـد اكـون مشغـول أو غيـر موجـود حاليـًا ؟!**\n"
        f"**⤶ ❨ لديـك {warns} مـن {total} تحذيـرات ⚠️❩**\n"
        "**⤶ لا تقـم بـ إزعاجـي وفي حال أزعجتني سـوف يتم حظـرك تلقائــيًا . . .**\n\n"
        f"**⤶ فقط قل سبب مجيئك وانتظـر الـرد ⏳**\n"
        f"**⤶ المتبقي قبل الحظر: {remaining}**"
    )

    try:
        old_id = state["message_cache"].get(uid)
        if old_id:
            try:
                await event.client.delete_messages(user.id, old_id)
            except Exception:
                pass

        msg = await event.reply(text)
        state["message_cache"][uid] = msg.id
    except Exception as e:
        LOGS.warning("تعذر إرسال رد الحماية: %s", e)

    _save()


def register(senzir):
    _load()

    @senzir.on(events.NewMessage(incoming=True))
    async def pm_protection_handler(event):
        await _private_protection(event)

    @senzir.on(
        events.NewMessage(
            outgoing=True,
            pattern=r"\.(الحمايه|الحماية)(?:\s+(تفعيل|تعطيل|تشغيل|ايقاف))?$",
        )
    )
    async def protection_toggle(event):
        action = event.pattern_match.group(2)

        if action in ("تفعيل", "تشغيل"):
            if state["enabled"]:
                return await _edit_delete(
                    event,
                    "** ⎉╎ امـر حمايـه الخـاص بالفعـل .. مُفعـل 🔐✅**",
                )

            state["enabled"] = True
            _save()
            return await _edit_delete(
                event,
                "** ⎉╎ تـم تفعيـل امـر حمايـة الخـاص بنجـاح 🔐✅**",
            )

        if action in ("تعطيل", "ايقاف"):
            if not state["enabled"]:
                return await _edit_delete(
                    event,
                    "** ⎉╎ امـر حمايـه الخـاص بالفعـل .. مُعطـل 🔓✅**",
                )

            state["enabled"] = False
            _save()
            return await _edit_delete(
                event,
                "** ⎉╎ تـم تعطيـل امـر حمايـة الخـاص بنجـاح 🔓✅**",
            )

        status = "مُفعّل 🔐" if state["enabled"] else "مُعطّل 🔓"
        await _edit_delete(
            event,
            f"**⎉╎ حمايـة الخـاص حاليـاً : {status}**\n\n"
            "**الاستخدام:**\n"
            "`.الحمايه تفعيل`\n"
            "`.الحمايه تعطيل`",
        )

    @senzir.on(
        events.NewMessage(
            outgoing=True,
            pattern=r"\.(سماح)(?:\s+([\s\S]+))?$",
        )
    )
    async def approve_pm(event):
        if not state["enabled"]:
            return await _edit_delete(
                event,
                "** ⎉╎لـيشتغل هذا الأمـر ...**\n"
                "** ⎉╎ يـجب تفعيـل امـر الحـمايـه اولاً **\n"
                "** ⎉╎بإرسـال `.الحمايه تفعيل`**",
            )

        user, reason = await _get_target(event, event.pattern_match.group(2))
        if not user:
            return await _edit_delete(
                event,
                "**⎉╎ أرسل الأمر بالرد على المستخدم أو اكتب المعرف/ID.**",
            )

        reason = (reason or "").strip() or "لم يذكر"

        state["approved"][str(user.id)] = {
            "first_name": getattr(user, "first_name", "") or "",
            "username": getattr(user, "username", "") or "",
            "reason": reason,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "user_id": user.id,
        }
        state["pmwarns"].pop(str(user.id), None)
        _remove_from_temp_lists(user.id)
        _save()

        await _clear_cached_message(event, user.id)

        await _edit_delete(
            event,
            f"**⎉╎المستخـدم** {_mention(user)}\n"
            "**⎉╎تـم السـمـاح لـه بـإرسـال الـرسـائـل 💬✓**\n"
            f"**⎉╎ الـسـبـب ❔ :** {reason}",
        )

    @senzir.on(
        events.NewMessage(
            outgoing=True,
            pattern=r"\.t(?:emp)?(?:a|approve)(?:\s+([\s\S]+))?$",
        )
    )
    async def tapprove_pm(event):
        user, reason = await _get_target(event, event.pattern_match.group(1))
        if not user:
            return await _edit_delete(
                event,
                "**⎉╎ أرسل الأمر بالرد على المستخدم أو اكتب المعرف/ID.**",
            )

        reason = (reason or "").strip() or "لم يذكر"

        if _approved(user.id):
            return await _edit_delete(
                event,
                f"**⎉╎المستخـدم** {_mention(user)} "
                "**موجود في قائمة السماح الدائمة ✅**",
            )

        if _temp_approved(user.id):
            return await _edit_delete(
                event,
                f"**⎉╎المستخـدم** {_mention(user)} "
                "**موجود بالفعل في قائمة السماح المؤقتة ✅**",
            )

        state["temporary_approved"].append(user.id)
        state["pmwarns"].pop(str(user.id), None)
        _remove_from_temp_lists(user.id)
        state["temporary_approved"].append(user.id)
        _save()

        await _clear_cached_message(event, user.id)

        await _edit_delete(
            event,
            f"**⎉╎المستخـدم** {_mention(user)} "
            "__تمت الموافقة عليه مؤقتاً__\n"
            f"**Reason :** __{reason}__",
        )

    @senzir.on(
        events.NewMessage(
            outgoing=True,
            pattern=r"\.(رف|رفض)(?:\s+([\s\S]+))?$",
        )
    )
    async def disapprove_pm(event):
        value = (event.pattern_match.group(2) or "").strip()

        if value == "الكل":
            state["approved"].clear()
            state["temporary_approved"].clear()
            _save()
            return await _edit_delete(
                event,
                "**⎉╎حــسـنـا تــم رفـض الـجـمـيـع .. بنجـاح 💯**",
            )

        user, reason = await _get_target(event, value)
        if not user:
            return await _edit_delete(
                event,
                "**⎉╎ أرسل الأمر بالرد على المستخدم أو اكتب المعرف/ID.**",
            )

        reason = reason.strip() or "لـم يـذكـر 💭"

        if _approved(user.id):
            state["approved"].pop(str(user.id), None)
            _save()
            await _edit_or_reply(
                event,
                f"**⎉╎المستخـدم** {_mention(user)}\n"
                "**⎉╎تـم رفـضـه مـن إرسـال الـرسـائـل ⚠️**\n"
                f"**⎉╎ الـسـبـب ❔ :** {reason}",
            )
        elif _temp_approved(user.id):
            _remove_from_temp_lists(user.id)
            _save()
            await _edit_or_reply(
                event,
                f"**⎉╎المستخـدم** {_mention(user)}\n"
                "**⎉╎تـم رفـضـه مـن إرسـال الـرسـائـل ⚠️**\n"
                f"**⎉╎ الـسـبـب ❔ :** {reason}",
            )
        else:
            await _edit_delete(
                event,
                f"**⎉╎المستخـدم** {_mention(user)}\n"
                "**⎉╎لــم تـتـم الـمـوافـقـة عـلـيـه مـسـبـقـاً ❕**",
            )

    @senzir.on(
        events.NewMessage(
            outgoing=True,
            pattern=r"\.بلوك(?:\s+([\s\S]+))?$",
        )
    )
    async def block_pm(event):
        user, reason = await _get_target(event, event.pattern_match.group(1))
        if not user:
            return await _edit_delete(
                event,
                "**⎉╎ أرسل الأمر بالرد على المستخدم أو اكتب المعرف/ID.**",
            )

        reason = (reason or "").strip() or "لـم يـذكـر 💭"

        state["pmwarns"].pop(str(user.id), None)
        state["approved"].pop(str(user.id), None)
        _remove_from_temp_lists(user.id)
        await _clear_cached_message(event, user.id)
        _save()

        await _block_user(event, user)

        await _edit_or_reply(
            event,
            f"**- المسـتخـدم :** {_mention(user)} "
            "**تم حظـره بنجـاح .. لايمكنـه ازعـاجـك الان**\n\n"
            f"**- السـبب :** {reason}",
        )

    @senzir.on(
        events.NewMessage(
            outgoing=True,
            pattern=r"\.الغاء بلوك(?:\s+([\s\S]+))?$",
        )
    )
    async def unblock_pm(event):
        user, reason = await _get_target(event, event.pattern_match.group(1))
        if not user:
            return await _edit_delete(
                event,
                "**⎉╎ أرسل الأمر بالرد على المستخدم أو اكتب المعرف/ID.**",
            )

        reason = (reason or "").strip() or "لـم يـذكـر 💭"
        await _unblock_user(event, user)

        await _edit_or_reply(
            event,
            f"**- المسـتخـدم :** {_mention(user)} "
            "**تم الغـاء حظـره بنجـاح .. يمكنـه التكلـم معـك الان**\n\n"
            f"**- السـبب :** {reason}",
        )

    @senzir.on(
        events.NewMessage(
            outgoing=True,
            pattern=r"\.المقبولين$",
        )
    )
    async def approved_list(event):
        if not state["enabled"]:
            return await _edit_delete(
                event,
                "** ⎉╎لـيشتغل هذا الأمـر ...**\n"
                "** ⎉╎ يـجب تفعيـل امـر الحـمايـه اولاً **",
            )

        if not state["approved"]:
            return await _edit_delete(
                event,
                "**- انت لـم توافـق على اي شخـص بعـد**",
            )

        text = "**- قائمـة المسمـوح لهـم ( المقبـوليـن ) :**\n\n"

        for item in state["approved"].values():
            username = (
                f"@{item['username']}"
                if item.get("username")
                else "بدون معرف"
            )
            text += (
                f"**• 👤 الاسـم :** "
                f"[{item.get('first_name') or 'بدون اسم'}]"
                f"(tg://user?id={item['user_id']})\n"
                f"**- الايـدي :** `{item['user_id']}`\n"
                f"**- المعـرف :** {username}\n"
                f"**- التـاريخ :** __{item.get('date', '')}__\n"
                f"**- السـبـب :** __{item.get('reason', '')}__\n\n"
            )

        await _edit_or_reply(event, text)

    LOGS.info("تم تسجيل ملف حماية الخاص مع senzir")
