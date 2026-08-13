from telethon import Button, events


def register(senzir):

    @senzir.on(
        events.NewMessage(
            outgoing=True,
            pattern=r"\.م1$"
        )
    )
    async def ms(event):
        await event.edit(
            """**
〠 اوامر الوقتي سورس البرنس & سينزر
⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆
لتفعيل الاسم الوقتي ⬅️ .اسم وقتي + الاسم
مثلا .اسم وقتي senzir
لايقاف الاسم الوقتي ⬅️ .ايقاف الاسم الوقتي**"""
        )

    @senzir.on(
        events.NewMessage(
            outgoing=True,
            pattern=r"\.م2$"
        )
    )
    async def ms2(event):
        text = """**
〠 اوامر حماية الخاص سورس البرنس & سينزر
⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆
- لتفعيل حماية الخاص ⇐ .الحمايه تفعيل

لايقاف حماية الخاص ⇐ .الحمايه تعطيل
⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆
**"""

        buttons = [
            [
                Button.url("👨‍💻 المطور سينزر", "https://t.me/senzir1"),
                Button.url("👨‍💻 المطور البرنس", "https://t.me/Albrans")
            ]
        ]

        await senzir.edit_message(
            event.chat_id,
            event.id,
            message=text,
            buttons=buttons
        )
