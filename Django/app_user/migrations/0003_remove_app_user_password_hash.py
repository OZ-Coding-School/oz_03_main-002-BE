# Generated by Django 5.0.7 on 2024-07-25 18:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app_user", "0002_alter_app_user_user_id"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="app_user",
            name="password_hash",
        ),
    ]
