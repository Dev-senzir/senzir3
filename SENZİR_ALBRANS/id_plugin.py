from telethon import events
from telethon.utils import pack_bot_file_id


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


def register(client, owner_id):

    @client.on(
        events.NewMessage(
            outgoing=True,
            pattern=r"\.(?:الايدي|id)(?:\s+(.+))?$"
        )
    )
    async def get_id(event):
        if event.sender_id != owner_id:
            return

        target = event.pattern_match.group(1)

        if target:
            try:
                entity = await client.get_entity(target.strip())

                name = (
                    getattr(entity, "first_name", None)
                    or getattr(entity, "title", None)
                    or getattr(entity, "username", None)
                    or "المستخدم"
                )

                await event.edit(
                    f"**⎉╎الاسم:** `{name}`\n"
                    f"**⎉╎الايدي:** `{entity.id}`"
                )

            except Exception as e:
                await event.edit(
                    f"**تعذر العثور على المستخدم/الدردشة:** `{e}`"
                )

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

            await event.edit(text)
            return

        await event.edit(
            f"**⎉╎ايدي الدردشة:** `{event.chat_id}`"
        )


    @client.on(
        events.NewMessage(
            outgoing=True,
            pattern=r"\.رابطه(?:\s+(.+))?$"
        )
    )
    async def permalink(event):
        if event.sender_id != owner_id:
            return

        arg = event.pattern_match.group(1)

        try:
            if event.is_reply and not arg:
                reply = await event.get_reply_message()

                if not reply or not reply.sender_id:
                    await event.edit("**لم أستطع تحديد المستخدم.**")
                    return

                user = await client.get_entity(reply.sender_id)
                custom_text = None

            elif arg:
                parts = arg.strip().split(maxsplit=1)
                user = await client.get_entity(parts[0])
                custom_text = parts[1] if len(parts) > 1 else None

            else:
                await event.edit(
                    "**استخدم `.رابطه` بالرد على المستخدم أو اكتب المعرف.**"
                )
                return

            name = _clean_name(user)
            text = custom_text or name

            await event.edit(
                f"[{text}](tg://user?id={user.id})"
            )

        except Exception as e:
            await event.edit(
                f"**تعذر العثور على المستخدم:** `{e}`"
            )


    @client.on(
        events.NewMessage(
            outgoing=True,
            pattern=r"\.اسمي$"
        )
    )
    async def my_name(event):
        if event.sender_id != owner_id:
            return

        user = await client.get_me()
        name = _clean_name(user)

        await event.edit(
            f"[{name}](tg://user?id={user.id})"
        )


    @client.on(
        events.NewMessage(
            outgoing=True,
            pattern=r"\.اسمه(?:\s+(.+))?$"
        )
    )
    async def his_name(event):
        if event.sender_id != owner_id:
            return

        arg = event.pattern_match.group(1)

        try:
            if event.is_reply and not arg:
                reply = await event.get_reply_message()

                if not reply or not reply.sender_id:
                    await event.edit("**لم أستطع تحديد المستخدم.**")
                    return

                user = await client.get_entity(reply.sender_id)
                custom_text = None

            elif arg:
                parts = arg.strip().split(maxsplit=1)
                user = await client.get_entity(parts[0])
                custom_text = parts[1] if len(parts) > 1 else None

            else:
                await event.edit(
                    "**استخدم `.اسمه` بالرد على المستخدم أو اكتب المعرف.**"
                )
                return

            name = _clean_name(user)
            text = custom_text or name

            await event.edit(
                f"[{text}](tg://user?id={user.id})"
            )

        except Exception as e:
            await event.edit(
                f"**تعذر العثور على المستخدم:** `{e}`"
            )
