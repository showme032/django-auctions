# Generated by Django 4.2.3 on 2023-08-23 13:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0008_alter_bid_bidder_alter_bid_listing"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bid",
            name="bidder",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="bids",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
