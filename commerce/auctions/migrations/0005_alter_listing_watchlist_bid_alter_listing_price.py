# Generated by Django 4.2.1 on 2023-05-27 16:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_rename_comments_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='watchList',
            field=models.ManyToManyField(blank=True, related_name='listingWatchlist', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bid', models.DecimalField(decimal_places=2, max_digits=5)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='UserBid', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='listing',
            name='price',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bidPrice', to='auctions.bid'),
        ),
    ]