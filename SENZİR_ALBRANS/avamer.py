from telethon import events

#𝗦𝗘𝗡𝗭𝗜𝗥
#𓆩 𝗔𝗟𝗕𝗥𝗔𝗡𝗦 𓆪
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
〠 اوامر الانتحال  سورس البرنس & سينزر
⋆┄─┄─┄─┄┄─┄─┄─┄┄⋆
- لــ الانتـحال ⇐ {`.انتحال` } بلرد ع مستخدم المراد انتحاله

لاعاده الحساب لوضعه الطبيعي ⇐ .اعادة 
⋆┄─┄─┄─┄┄─┄─┄─┄┄⋆

👨‍💻 [𓆩 𝗦𝗘𝗡𝗭𝗜𝗥 𓆪](https://t.me/senzir1)
👨‍💻 [𓆩 𝗔𝗟𝗕𝗥𝗔𝗡𝗦 𓆪](https://t.me/Albrans)
**""",
            parse_mode="md"
        )

    @senzir.on(
    events.NewMessage(
        outgoing=True,
        pattern=r"\.م4$"
    )
)
async def ms4(event):
    await event.edit(
        """**
〠 اوامر الاشتراك الاجباري في الخاص سورس البرنس & سينزر
⋆┄─┄─┄─┄┄─┄─┄─┄┄⋆
- او المجموعة لتفعيل الاشتراك الاجباري ⇐ .`اشتراك اجباري` + معرف القناة

- لايقاف الاشتراك الاجباري ⇐ `.ايقاف الاشتراك الاجباري`

- ملاحظه: يجب أن يكون الحساب مشرف في القناة او المجموعة اولا
واذا كانت القناة/المجموعة خاصه تقوم باستخدام الايدي
⋆┄─┄─┄─┄┄─┄─┄─┄┄⋆
**""",
        parse_mode="md"
    )
        )
