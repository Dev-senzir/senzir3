@senzir.on(events.NewMessage(outgoing=True,pattern='.م1'))
async def ms (event):
		await event.edit("""**
〠 اوامر الوقتي سورس البرنس & سينزر
⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆
لتفعيل الاسم الوقتي ⬅️ .اسم وقتي + الاسم
لايقاف الاسم الوقتي ⬅️ .ايقاف الاسم الوقتي**""")
