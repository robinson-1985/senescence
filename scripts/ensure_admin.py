import os
import sys

import django


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "senescence.settings")
    django.setup()

    from django.contrib.auth import get_user_model

    username = os.getenv("ADMIN_USERNAME")
    password = os.getenv("ADMIN_PASSWORD")
    email = os.getenv("ADMIN_EMAIL", "")

    if not username or not password:
        print("ADMIN_USERNAME/ADMIN_PASSWORD not set; skipping admin ensure.")
        return 0

    User = get_user_model()

    user, created = User.objects.get_or_create(
        username=username,
        defaults={"email": email},
    )

    user.is_staff = True
    user.is_superuser = True
    if email:
        user.email = email

    user.set_password(password)
    user.save()

    print(f"Admin ensured: {username} (created={created})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
