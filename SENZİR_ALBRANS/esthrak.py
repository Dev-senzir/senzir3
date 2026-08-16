import os
import sqlite3

from telethon import events
from telethon.tl import functions
from telethon.tl.types import (
    ChannelParticipant,
    ChannelParticipantAdmin,
    ChannelParticipantCreator,
)
from telethon.errors import UserNotParticipantError

from .vars import mention


DB_FILE = os.path.join(
    os.path.dirname(__file__),
    "esthrak.db"
)


def get_db():
    db = sqlite3.connect(DB_FILE)

    db.execute("""
        CREATE TABLE IF NOT EXISTS الاشتراك_الاجباري (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            المعرف TEXT NOT NULL
        )
    """)

    db.commit()
    return db


def get_channel():
    db = get_db()

    row = db.execute(
        "SELECT المعرف FROM الاشتراك_الاجباري WHERE id = 1"
    ).fetchone()

    db.close()

    return row[0] if row else None


def set_channel(channel):
    db = get_db()

    db.execute("""
        INSERT OR REPLACE INTO الاشتراك_الاجباري
        (id, المعرف)
        VALUES (1, ?)
    """, (str(channel),))

    db.commit()
    db.close()


def disable_channel():
    db = get_db()

    db.execute(
        "DELETE FROM الاشتراك_الاجباري"
    )

    db.commit()
    db.close()


def normalize_channel(value):
    value = value.strip()

    if value.startswith("@"):
        return value

    if value.startswith("-100"):
        try:
            return int(value)
        except ValueError:
            return None

    return None


async def check_owner_permission(senzir, albrans):
    try:
        entity = await senzir.get_entity(albrans)
        me = await senzir.get_me()

        participant = await senzir(
            functions.channels.GetParticipantRequest(
                channel=entity,
                participant=me.id
            )
        )

        membership = participant.participant

        if isinstance(
            membership,
            (
                ChannelParticipantCreator,
                ChannelParticipantAdmin,
            )
        ):
            return True, entity

        return False, entity

    except Exception as e:
        print(
            f"[esthrak] Permission check error: {e}"
        )
        return False, None


async def is_subscribed(senzir, albrans, user_id):
    try:
        entity = await senzir.get_entity(albrans)

        participant = await senzir(
            functions.channels.GetParticipantRequest(
                channel=entity,
                participant=user_id
            )
        )

        membership = participant.participant

        if isinstance(
            membership,
            (
                ChannelParticipant,
                ChannelParticipantAdmin,
                ChannelParticipantCreator,
            )
        ):
            return True

        return False

    except UserNotParticipantError:
        return False

    except Exception as e:
        print(
            f"[esthrak] Subscription check error: {e}"
        )
        return False


def register(senzir):

    @senzir.on(
        events.NewMessage(
            outgoing=True,
            pattern=r"\.اشتراك اجباري(?:\s+([\s\S]+))?$"
        )
    )
    async def enable(event):

        value = event.pattern_match.group(1)

        if not value:
            return await event.edit(
                "**⎉╎ضع رابط القناة أو المجموعة أولًا.**\n\n"
                "⎉╎للعامة:\n"
                "`.اشتراك اجباري @username`\n\n"
                "⎉╎للخاصة:\n"
                "`.اشتراك اجباري -1001234567890`"
            )

        albrans = normalize_channel(value)

        if albrans is None:
            return await event.edit(
                "**⛔️ المعرف غير صحيح.**\n\n"
                "⎉╎استخدم `@username` للقناة أو المجموعة العامة.\n"
                "⎉╎أو استخدم `-100xxxxxxxxxx` للقناة أو المجموعة الخاصة."
            )

        await event.edit(
            "**⎉╎جاري التحقق من القناة/المجموعة... ⏳**"
        )

        allowed, entity = await check_owner_permission(
            senzir,
            albrans
        )

        if entity is None:
            return await event.edit(
                "**⛔️ لم أستطع الوصول إلى القناة أو المجموعة.**\n\n"
                "تأكد من صحة المعرف وأن الحساب موجود فيها."
            )

        if not allowed:
            return await event.edit(
                "**⛔️ لا يمكن تفعيل الاشتراك الإجباري.**\n\n"
                "⎉╎يجب أن يكون حساب السورس مشرفًا أو مالكًا فيها."
            )

        if getattr(entity, "megagroup", False):
            place_type = "المجموعة"
        else:
            place_type = "القناة"

        set_channel(albrans)

        await event.edit(
            f"**⎉╎تم تفعيل الاشتراك الإجباري ✅**\n\n"
            f"⎉╎النوع: {place_type}\n"
            f"⎉╎المعرف: `{albrans}`"
        )

    @senzir.on(
        events.NewMessage(
            outgoing=True,
            pattern=r"\.ايقاف الاشتراك الاجباري$"
        )
    )
    async def disable(event):

        if get_channel() is None:
            return await event.edit(
                "**⎉╎الاشتراك الإجباري غير مفعل أصلًا.**"
            )

        disable_channel()

        await event.edit(
            "**⎉╎تم إيقاف الاشتراك الإجباري ✅**"
        )

    @senzir.on(
        events.NewMessage(
            incoming=True
        )
    )
    async def check_messages(event):

        if not event.is_private:
            return

        albrans = get_channel()

        if not albrans:
            return

        user = await event.get_sender()

        if not user:
            return

        if getattr(user, "bot", False):
            return

        if getattr(user, "deleted", False):
            return

        me = await senzir.get_me()

        if user.id == me.id:
            return

        try:
            entity = await senzir.get_entity(albrans)
        except Exception as e:
            print(
                f"[esthrak] Entity error: {e}"
            )
            return

        if getattr(entity, "megagroup", False):
            place_type = "المجموعة"
        else:
            place_type = "القناة"

        subscribed = await is_subscribed(
            senzir,
            albrans,
            user.id
        )

        if subscribed:
            return

        try:
            await event.delete()
        except Exception as e:
            print(
                f"[esthrak] Delete error: {e}"
            )

        text = (
            f"**مرحبا عزيزي {mention(user)} .**\n\n"
            f"⎉╎يجب عليك الاشتراك في هذه {place_type} أولًا للتمكن من مراسلتي.\n\n"
            f"⎉╎المعرف: `{albrans}`\n\n"
            "⎉╎بعد الاشتراك أرسل رسالتك مرة أخرى "
            "ليتم التحقق منك تلقائيًا ✅"
        )

        try:
            await senzir.send_message(
                event.chat_id,
                text
            )
        except Exception as e:
            print(
                f"[esthrak] Send error: {e}"
            )
