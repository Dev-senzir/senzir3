from telethon import events
from telethon.tl import functions
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.photos import (
    UploadProfilePhotoRequest,
    DeletePhotosRequest,
)


def register(senzir):

    original_data = {
        "first_name": None,
        "last_name": None,
        "bio": None,
        "photo": None,
    }

    saved = False

    @senzir.on(
        events.NewMessage(
            outgoing=True,
            pattern=r"\.(?:انتحال|نسخ)$"
        )
    )
    async def impersonate(event):
        nonlocal saved

        if not event.is_reply:
            await event.edit(
                "**يجب الرد على شخص لاستخدام هذا الأمر.**"
            )
            return

        replied = await event.get_reply_message()
        user = await replied.get_sender()

        if not user:
            await event.edit(
                "**تعذر العثور على الشخص.**"
            )
            return

        # حفظ بيانات الحساب الأصلية
        if not saved:
            me = await senzir.get_me()

            original_data["first_name"] = me.first_name or ""
            original_data["last_name"] = me.last_name or ""

            full_me = await senzir(
                GetFullUserRequest("me")
            )

            original_data["bio"] = (
                full_me.full_user.about or ""
            )

            original_data["photo"] = (
                await senzir.download_profile_photo(
                    "me",
                    file=bytes
                )
            )

            saved = True

        # بيانات الشخص
        first_name = user.first_name or ""
        last_name = user.last_name or ""

        full_user = await senzir(
            GetFullUserRequest(user.id)
        )

        # الحد الأقصى للبايو
        bio = (full_user.full_user.about or "")[:70]

        # تغيير الاسم والكنية والبايو
        await senzir(
            functions.account.UpdateProfileRequest(
                first_name=first_name,
                last_name=last_name,
                about=bio
            )
        )

        # نسخ الصورة
        photo = await senzir.download_profile_photo(
            user,
            file=bytes
        )

        if photo:
            uploaded = await senzir.upload_file(photo)

            await senzir(
                UploadProfilePhotoRequest(
                    file=uploaded
                )
            )

        await event.edit(
            "**𓆰 تم انتحال الشخص بنجاح ✅**"
        )

    @senzir.on(
        events.NewMessage(
            outgoing=True,
            pattern=r"\.اعادة$"
        )
    )
    async def revert(event):
        nonlocal saved

        if not saved:
            await event.edit(
                "**لا توجد بيانات محفوظة لإعادة الحساب.**"
            )
            return

        # حذف الصورة الحالية
        photos = await senzir.get_profile_photos(
            "me",
            limit=1
        )

        if photos:
            await senzir(
                DeletePhotosRequest(
                    id=[photos[0]]
                )
            )

        # إعادة الاسم والكنية والبايو
        await senzir(
            functions.account.UpdateProfileRequest(
                first_name=original_data["first_name"],
                last_name=original_data["last_name"],
                about=original_data["bio"]
            )
        )

        # إعادة الصورة الأصلية
        if original_data["photo"]:
            uploaded = await senzir.upload_file(
                original_data["photo"]
            )

            await senzir(
                UploadProfilePhotoRequest(
                    file=uploaded
                )
            )

        # تصفير البيانات
        original_data["first_name"] = None
        original_data["last_name"] = None
        original_data["bio"] = None
        original_data["photo"] = None

        saved = False

        await event.edit(
            "**𓆰 تمت إعادة الحساب لوضعه الأصلي ✅**"
        )
