# Generated by Django 4.2.1 on 2023-05-26 15:52

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='imageUrl',
            new_name='imageurl',
        ),
        migrations.AddField(
            model_name='listing',
            name='watchList',
            field=models.ManyToManyField(blank=True, null=True, related_name='users', to=settings.AUTH_USER_MODEL),
        ),
    ]
