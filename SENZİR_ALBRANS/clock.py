import asyncio
import logging
import time
## ©️ جميع الحقوق محفوظة لــ المطور سينــزر 2025 ©️ ##
from telethon import events, functions
from telethon.errors import FloodWaitError
## ©️ جميع الحقوق محفوظة لــ المطور سينــزر 2025 ©️ ##

def register(senzir):
    clock_running = False
    clock_name = "𝐄𝐋𝐄𝐒𝐘𝐄𝐃"
    original_name = None

    DEL_TIME_OUT = 60
## ©️ جميع الحقوق محفوظة لــ المطور سينــزر 2025 ©️ ##
    normzltext = "0123456789"
    namerzfont = "𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗"

    LOGS = logging.getLogger(__name__)
## ©️ جميع الحقوق محفوظة لــ المطور سينــزر 2025 ©️ ##
    @senzir.on(
        events.NewMessage(
            outgoing=True,
            pattern=r"\.اسم وقتي(?:\s+(.+))?$"
        )
    )
    async def start_clock(event):
        nonlocal clock_running, clock_name, original_name

        if clock_running:
            await event.edit("تم تشغيله من قبل")
            await asyncio.sleep(15)
            try:
                await event.delete()
            except Exception:
                pass
            return

        me = await senzir.get_me()
        original_name = me.first_name

        new_name = event.pattern_match.group(1)

        if new_name:
            clock_name = new_name.strip()
        else:
            clock_name = "𝐄𝐋𝐄𝐒𝐘𝐄𝐃"

        clock_running = True

        ## ©️ جميع الحقوق محفوظة لــ المطور سينــزر 2025 ©️ ##
        await event.edit("تم تشغيل بنجاح")
        await asyncio.sleep(15)
        try:
            await event.delete()
        except Exception:
            pass

        while clock_running:
            HM = time.strftime("%I:%M")

            for normal in HM:
                if normal in normzltext:
                    namefont = namerzfont[normzltext.index(normal)]
                    HM = HM.replace(normal, namefont)

            name = f"{clock_name} | {HM}"

            try:
                await senzir(
                    functions.account.UpdateProfileRequest(
                        first_name=name
                    )
                )
            except FloodWaitError as ex:
                LOGS.warning(str(ex))
                await asyncio.sleep(ex.seconds)

            await asyncio.sleep(DEL_TIME_OUT)

    @senzir.on(
        events.NewMessage(
            outgoing=True,
            pattern=r"\.ايقاف الاسم الوقتي$"
        )
    )
    async def stop_clock(event):
        nonlocal clock_running, original_name, clock_name

        if not clock_running:
            await event.edit("تم ايقافه من قبل")
            await asyncio.sleep(15)
            try:
                await event.delete()
            except Exception:
                pass
            return

        clock_running = False

        if original_name is not None:
            try:
                await senzir(
                    functions.account.UpdateProfileRequest(
                        first_name=original_name
                    )
                )
            except FloodWaitError as ex:
                LOGS.warning(str(ex))
                await asyncio.sleep(ex.seconds)

        await event.edit("تم الايقاف")
        await asyncio.sleep(15)

        try:
            await event.delete()
        except Exception:
            pass

        original_name = None
        clock_name = "𝐄𝐋𝐄𝐒𝐘𝐄𝐃"
        ## ©️ جميع الحقوق محفوظة لــ المطور سينــزر 2025 ©️ ##
