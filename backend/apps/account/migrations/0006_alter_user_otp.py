# Generated by Django 5.1 on 2024-12-20 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0005_rename_opt_user_otp"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="otp",
            field=models.CharField(blank=True, max_length=8, null=True),
        ),
    ]
