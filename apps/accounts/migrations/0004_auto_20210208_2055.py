# Generated by Django 3.0.2 on 2021-02-08 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0003_auto_20210208_2046"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="last_updated_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
