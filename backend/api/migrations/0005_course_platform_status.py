# Generated by Django 5.1 on 2024-09-07 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0004_category_active"),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="platform_status",
            field=models.CharField(
                choices=[
                    ("Published", "Published"),
                    ("Pending", "Pending"),
                    ("Draft", "Draft"),
                ],
                default="Published",
                max_length=255,
            ),
            preserve_default=False,
        ),
    ]