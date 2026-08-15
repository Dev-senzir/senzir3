from telethon import events


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
لايقاف الاسم الوقتي ⬅️ .ايقاف الاسم الوقتي**""",
            parse_mode="md"
        )

    @senzir.on(
        events.NewMessage(
            outgoing=True,
            pattern=r"\.م2$"
        )
    )
    async def ms2(event):
        await event.edit(
            """**
〠 اوامر حماية الخاص سورس البرنس & سينزر
⋆┄─┄─┄─┄┄─┄─┄─┄┄⋆
- لتفعيل حماية الخاص ⇐ .الحمايه تفعيل

لايقاف حماية الخاص ⇐ .الحمايه تعطيل
⋆┄─┄─┄─┄┄─┄─┄─┄┄⋆

👨‍💻 [المطور سينزر](https://t.me/senzir1)
👨‍💻 [المطور البرنس](https://t.me/Albrans)
**""",
            parse_mode="md"
        )
