# Generated by Django 3.0.2 on 2021-02-08 20:46

from django.db import migrations
from django.conf import settings


class Migration(migrations.Migration):
    def create_default_admin(self, schema_editor):
        from apps.accounts.models import User

        admin = User()
        admin.email = "hendrik@blankontech.com"
        admin.first_name = "Hendrik"
        admin.last_name = "Tukunang"
        admin.is_staff = True
        admin.is_superuser = True
        admin.set_password(settings.DEFAULT_ADMIN_PASSWORD)
        admin.save()

    dependencies = [
        ("accounts", "0002_auto_20210208_2045"),
    ]

    operations = [
        migrations.RunPython(create_default_admin),
    ]