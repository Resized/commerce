# Generated by Django 4.2.2 on 2023-07-01 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_alter_auctionlisting_image_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlisting',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
