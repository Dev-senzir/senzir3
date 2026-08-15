## ©️ جميع الحقوق محفوظة لــ المطور سينــزر 2025 ©️ ##

import os
import tempfile

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

    async def safe_edit(event, text):
        try:
            await event.edit(text)
        except Exception as e:
            print(f"[impersonate] Edit error: {e}")

    @senzir.on(
        events.NewMessage(
            outgoing=True,
            pattern=r"\.(?:انتحال|نسخ)$"
        )
    )
    async def impersonate(event):
        nonlocal saved

        if not event.is_reply:
            await safe_edit(
                event,
                "**يجب الرد على شخص لاستخدام هذا الأمر.**"
            )
            return

        replied = await event.get_reply_message()
        user = await replied.get_sender()

        if not user:
            await safe_edit(
                event,
                "**تعذر العثور على الشخص.**"
            )
            return

        try:

            ## ©️ جميع الحقوق محفوظة لــ المطور سينــزر 2025 ©️ ##
            if not saved:

                me = await senzir.get_me()

                original_data["first_name"] = (
                    me.first_name or ""
                )

                original_data["last_name"] = (
                    me.last_name or ""
                )

                full_me = await senzir(
                    GetFullUserRequest("me")
                )

                original_data["bio"] = (
                    full_me.full_user.about or ""
                )

                ## ©️ جميع الحقوق محفوظة لــ المطور سينــزر 2025 ©️ ##
                original_photo = os.path.join(
                    tempfile.gettempdir(),
                    "senzir_original_profile.jpg"
                )

                try:
                    photo_path = await senzir.download_profile_photo(
                        "me",
                        file=original_photo
                    )

                    if photo_path and os.path.exists(photo_path):
                        original_data["photo"] = photo_path
                    else:
                        original_data["photo"] = None

                except Exception as e:
                    print(
                        f"[impersonate] Save original photo error: {e}"
                    )
                    original_data["photo"] = None

                saved = True

            ## ©️ جميع الحقوق محفوظة لــ المطور سينــزر 2025 ©️ ##
            first_name = user.first_name or ""
            last_name = user.last_name or ""

            full_user = await senzir(
                GetFullUserRequest(user.id)
            )

            ## ©️ جميع الحقوق محفوظة لــ المطور سينــزر 2025 ©️ ##
            bio = (full_user.full_user.about or "")[:70]

            
            await senzir(
                functions.account.UpdateProfileRequest(
                    first_name=first_name,
                    last_name=last_name,
                    about=bio
                )
            )

            
            photo_success = False

            target_photo = os.path.join(
                tempfile.gettempdir(),
                "senzir_target_profile.jpg"
            )

            try:
                photo_path = await senzir.download_profile_photo(
                    user,
                    file=target_photo
                )

                if photo_path and os.path.exists(photo_path):

                    uploaded = await senzir.upload_file(
                        photo_path
                    )

                    await senzir(
                        UploadProfilePhotoRequest(
                            file=uploaded
                        )
                    )

                    photo_success = True

                    try:
                        os.remove(photo_path)
                    except Exception:
                        pass

            except Exception as e:
                print(
                    f"[impersonate] Copy photo error: {e}"
                )

            ## ©️ جميع الحقوق محفوظة لــ المطور سينــزر 2025 ©️ ##
            if photo_success:
                await safe_edit(
                    event,
                    "**𓆰 تم انتحال الشخص بنجاح ✅**"
                )
            else:
                await safe_edit(
                    event,
                    "**𓆰 تم انتحال الاسم والبايو بنجاح ✅**\n"
                    "**⚠️ تعذر نسخ صورة الحساب.**"
                )

        except Exception as e:

            print(
                f"[impersonate] Impersonate error: {e}"
            )

            await safe_edit(
                event,
                f"**حدث خطأ أثناء الانتحال ❌**\n`{e}`"
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
            await safe_edit(
                event,
                "**لا توجد بيانات محفوظة لإعادة الحساب.**"
            )
            return

        try:

            ## ©️ جميع الحقوق محفوظة لــ المطور سينــزر 2025 ©️ ##
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

            ## ©️ جميع الحقوق محفوظة لــ المطور سينــزر 2025 ©️ ##
            await senzir(
                functions.account.UpdateProfileRequest(
                    first_name=original_data["first_name"],
                    last_name=original_data["last_name"],
                    about=original_data["bio"]
                )
            )

            ## ©️ جميع الحقوق محفوظة لــ المطور سينــزر 2025 ©️ ##
            photo_success = False

            original_photo = original_data["photo"]

            if original_photo and os.path.exists(original_photo):

                try:
                    uploaded = await senzir.upload_file(
                        original_photo
                    )

                    await senzir(
                        UploadProfilePhotoRequest(
                            file=uploaded
                        )
                    )

                    photo_success = True

                except Exception as e:
                    print(
                        f"[impersonate] Restore photo error: {e}"
                    )

            
            if original_photo and os.path.exists(original_photo):
                try:
                    os.remove(original_photo)
                except Exception:
                    pass

            
            original_data["first_name"] = None
            original_data["last_name"] = None
            original_data["bio"] = None
            original_data["photo"] = None

            saved = False

            ## ©️ جميع الحقوق محفوظة لــ المطور سينــزر 2025 ©️ ##
            if photo_success:
                await safe_edit(
                    event,
                    "**𓆰 تمت إعادة الحساب لوضعه الأصلي بنجاح ✅**"
                )
            else:
                await safe_edit(
                    event,
                    "**𓆰 تمت إعادة الاسم والبايو بنجاح ✅**\n"
                    "**⚠️ تعذر إعادة صورة الحساب.**"
                )

        except Exception as e:

            print(
                f"[impersonate] Revert error: {e}"
            )

            await safe_edit(
                event,
                f"**حدث خطأ أثناء إعادة الحساب ❌**\n`{e}`"
            )
