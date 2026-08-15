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

    @senzir.on(
        events.NewMessage(
            outgoing=True,
            pattern=r"\.م3$"
        )
    )
    async def ms3(event):
        await event.edit(
            """**
〠 اوامر الانتحال الخاص سورس البرنس & سينزر
⋆┄─┄─┄─┄┄─┄─┄─┄┄⋆
- لــ الانتـحال ⇐ {.انتحال } بلرد ع مستخدم المراد انتحاله

لاعاده الحساب لوضعه الطبيعي ⇐ .اعادة 
⋆┄─┄─┄─┄┄─┄─┄─┄┄⋆

👨‍💻 [𓆩 𝗦𝗘𝗡𝗭𝗜𝗥 𓆪](https://t.me/senzir1)
👨‍💻 [𓆩 𝗔𝗟𝗕𝗥𝗔𝗡𝗦 𓆪](https://t.me/Albrans)
**""",
            parse_mode="md"
        )
