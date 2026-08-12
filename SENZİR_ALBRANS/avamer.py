from telethon import events


def register(senzir):

    @senzir.on(
        events.NewMessage(
            outgoing=True,
            pattern=r"\.م1$"
        )
    )
    async def ms(event):
        await event.edit("""**
〠 اوامر الوقتي سورس البرنس & سينزر
⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆
لتفعيل الاسم الوقتي ⬅️ .اسم وقتي + الاسم
مثلا .اسم وقتي senzir
لايقاف الاسم الوقتي ⬅️ .ايقاف الاسم الوقتي**""")
