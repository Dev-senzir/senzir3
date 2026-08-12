from telethon import events
from telethon.utils import pack_bot_file_id

# يستخدم نفس TelegramClient الموجود في senzir.py
# لا يوجد تسجيل دخول أو TelegramClient جديد هنا.
from .senzir import senzir, onersenzir_id


def _clean_name(user):
    if not user:
        return "المستخدم"
    first = getattr(user, "first_name", None)
    username = getattr(user, "username", None)
    if first:
        return first.replace("\u2060", "")
    if username:
        return f"@{username}"
    return "المستخدم"


@senzir.on(events.NewMessage(outgoing=False, pattern=r"\.(?:الايدي|id)(?:\s+(.+))?$"))
async def get_id(event):
    # يسمح باستخدام: .الايدي / .id / .الايدي @username
    input_str = event.pattern_match.group(1)

    # حماية اختيارية: نفس مالك السورس الحالي فقط
    sender = await event.get_sender()
    if sender and sender.id != onersenzir_id:
        return

    if input_str:
        try:
            entity = await senzir.get_entity(input_str.strip())
            title = (
                getattr(entity, "first_name", None)
                or getattr(entity, "title", None)
                or getattr(entity, "username", None)
                or str(entity.id)
            )
            await event.reply(
                f"**⎉╎الاسم:** `{title}`\n**⎉╎الايدي:** `{entity.id}`"
            )
        except Exception as e:
            await event.reply(f"**تعذر العثور على المستخدم/الدردشة:** `{e}`")
        return

    if event.is_reply:
        reply = await event.get_reply_message()
        text = (
            f"**⎉╎ايدي الدردشة:** `{event.chat_id}`\n\n"
            f"**⎉╎ايدي المستخدم:** `{reply.sender_id}`"
        )

        if reply.media:
            try:
                file_id = pack_bot_file_id(reply.media)
                text += f"\n\n**⎉╎ايدي الميديا:** `{file_id}`"
            except Exception:
                pass

        await event.reply(text)
        return

    await event.reply(f"**⎉╎ايدي الدردشة:** `{event.chat_id}`")


async def _resolve_user(event, arg=None):
    # يدعم الرد أو username أو numeric id
    if event.is_reply and not arg:
        reply = await event.get_reply_message()
        if reply and reply.sender_id:
            try:
                return await senzir.get_entity(reply.sender_id), None
            except Exception:
                return None, None

    if arg:
        arg = arg.strip()
        # يسمح بكتابة + نص مخصص بعد المعرف:
        # .رابطه @user النص
        parts = arg.split(maxsplit=1)
        target = parts[0]
        custom = parts[1] if len(parts) > 1 else None
        try:
            return await senzir.get_entity(target), custom
        except Exception as e:
            await event.reply(f"**تعذر العثور على المستخدم:** `{e}`")
            return None, None

    return None, None


@senzir.on(events.NewMessage(outgoing=False, pattern=r"\.رابطه(?:\s+(.+))?$"))
async def permalink(event):
    sender = await event.get_sender()
    if sender and sender.id != onersenzir_id:
        return

    arg = event.pattern_match.group(1)
    user, custom = await _resolve_user(event, arg)

    if not user:
        await event.reply("**استخدم `.رابطه` بالرد على المستخدم أو اكتب المعرف.**")
        return

    name = _clean_name(user)
    text = custom or name
    await event.reply(f"[{text}](tg://user?id={user.id})")


@senzir.on(events.NewMessage(outgoing=False, pattern=r"\.اسمي$"))
async def my_name_link(event):
    sender = await event.get_sender()
    if sender and sender.id != onersenzir_id:
        return

    user = await senzir.get_me()
    name = _clean_name(user)
    await event.reply(f"[{name}](tg://user?id={user.id})")


@senzir.on(events.NewMessage(outgoing=False, pattern=r"\.اسمه(?:\s+(.+))?$"))
async def his_name_link(event):
    sender = await event.get_sender()
    if sender and sender.id != onersenzir_id:
        return

    arg = event.pattern_match.group(1)
    user, custom = await _resolve_user(event, arg)

    if not user:
        await event.reply("**استخدم `.اسمه` بالرد على المستخدم أو اكتب المعرف.**")
        return

    name = _clean_name(user)
    text = custom or name
    await event.reply(f"[{text}](tg://user?id={user.id})")
