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
        await event.edit(
            "اختبار الأزرار",
            buttons=[
                [
                    Button.url(
                        "سينزر",
                        "https://t.me/senzir1"
                    ),
                    Button.url(
                        "البرنس",
                        "https://t.me/Albrans"
                    )
                ]
            ]
        )
