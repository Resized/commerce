# Generated by Django 4.2.2 on 2023-07-01 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_alter_auctionlisting_image_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='image_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
