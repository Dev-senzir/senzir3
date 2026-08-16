from telethon import events

from .vars_sql import set_var


def register(senzir):

    @senzir.on(
        events.NewMessage(
            outgoing=True,
            pattern=r"\.اضف كليشة الاشتراك الاجباري(?:\s+(.+))$"
        )
    )
    async def change_subscription_text(event):

        text = event.pattern_match.group(1)

        if not text:
            return await event.edit(
                "**⛔️ اكتب الكليشة بعد الأمر.**"
            )

        set_var(
            "subscription_text",
            text.replace("\\n", "\n")
        )

        await event.edit(
            "**⎉╎تم تغيير كليشة الاشتراك الإجباري ✅**"
        )
