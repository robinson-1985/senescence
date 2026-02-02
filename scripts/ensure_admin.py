import os
import django


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "senescence.settings")
    django.setup()

    from django.contrib.auth import get_user_model
    
    User = get_user_model()

    username = os.getenv("ADMIN_USERNAME", "admin")
    email = os.getenv("ADMIN_EMAIL", "admin@example.com")
    password = os.getenv("ADMIN_PASSWORD")

    if not password:
        raise SystemExit("ADMIN_PASSWORD não definida nas variáveis do Railway.")

        user, created = User.objects.get_or_create(username=username, defaults={"email": email})

        user.email = email
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()

        print(f"[OK] Admin garantido: {username} (created={created})")
