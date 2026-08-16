
def mention(user):
    return f"[{user.first_name or 'المستخدم'}](tg://user?id={user.id})"


def username(user):
    return f"@{user.username}" if user.username else "لا يوجد"


def userid(user):
    return str(user.id)


def firstname(user):
    return user.first_name or ""


def lastname(user):
    return user.last_name or ""


def fullname(user):
    first = user.first_name or ""
    last = user.last_name or ""
    return f"{first} {last}".strip()


def user_link(user):
    name = user.first_name or "المستخدم"
    return f"[{name}](tg://user?id={user.id})"


def user_id(user):
    return user.id


def user_username(user):
    return user.username or ""
