# Generated by Django 3.0.2 on 2021-02-08 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("todos", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="todo",
            name="last_updated_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
