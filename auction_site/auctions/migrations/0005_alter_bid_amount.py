# Generated by Django 5.1.4 on 2025-01-01 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0004_notification"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bid",
            name="amount",
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]