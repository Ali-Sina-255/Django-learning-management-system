# Generated by Django 5.1 on 2024-09-07 18:04

import shortuuid.django_fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0006_rename_counter_cart_country"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cart",
            name="cart_id",
            field=shortuuid.django_fields.ShortUUIDField(
                alphabet="1234567890", length=6, max_length=30, prefix=""
            ),
        ),
    ]
