from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        User = get_user_model()
        
        username = os.environ.get("ADMIN_USER", "admin")
        email = os.environ.get("ADMIN_EMAIL", "admin@admin.com")
        password = os.environ.get("ADMIN_PASS", "admin123")

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            print("Superuser criado com sucesso!")
        else:
            print("Superuser já existe.")
