# Generated by Django 5.1 on 2024-09-07 18:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0005_course_platform_status"),
    ]

    operations = [
        migrations.RenameField(
            model_name="cart",
            old_name="counter",
            new_name="country",
        ),
    ]
