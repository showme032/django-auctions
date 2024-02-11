# Generated by Django 4.2.3 on 2023-08-24 10:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0010_comment_alter_bid_bidder_delete_comments"),
    ]

    operations = [
        migrations.AlterField(
            model_name="listing",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="items",
                to="auctions.category",
            ),
        ),
    ]
